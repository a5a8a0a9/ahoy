# System Libs
import logging as log
import getpass
import datetime
import re
import os
import shutil
import xlwt
import pickle
from os.path import basename, join, splitext, isfile
# External Libs
from pdkutil.database import SqlDatabase
from pdkutil.mailservice import SendMail
from drmlib.compare import DrmDiff, DiffStat
import pymysql
import pymysql.cursors

# Internal Libs
from server.diff_report import (
    DrmDiffReportParser, DrmDiffReportParser2, Rule
)
from server.path import relative_path, db_path, report_path

class RevisionDatabase(SqlDatabase):
    """docstring for RevisionDatabase"""
    # def __init__(self):
    #     super(RevisionDatabase, self).__init__(db_path())

    def __init__(self):
        self._con = pymysql.connect(
            host='10.234.8.22',
            user='drmrev',
            # passwd='pdkd',
            db='DRMrevision_uat',
            connect_timeout= 6000,
            cursorclass=pymysql.cursors.DictCursor,
            )
        self._cursor = self._con.cursor()
        # self._con.ping(reconnect=True)
        print(self._cursor)

    def execute(self, sql):
        return self._cursor.execute(sql)

    def executescript(self, sql):
        return self._cursor.executescript(sql)

    def create_tables(self):
        sql = relative_path("create_table.sql")
        try:
            with open(sql) as f:
                sql_scripts = f.read()
            self._cursor.executescript(sql_scripts)
        except Exception as e:
            log.error(e)

    def put_data(self, table, **kwargs):
        """ Insert data into given table and commit table after that.
        [Input]
            table: string: table name to insert data
            **kwargs: key-value pairs which is <column, value>
        [Return]
            Int, the last inserted ID.
        """
        sql = "INSERT INTO %s (" % table
        for key in kwargs:
            sql += "%s," % key
        sql = sql.rstrip(",") + ") VALUES ("
        for key in kwargs:
            sql += "%s,"
        sql = sql.rstrip(",") + ")"
        log.info(sql)
        ls = list(kwargs.values())
        self._cursor.execute(sql, (ls))
        _id = self._cursor.lastrowid
        self._con.commit()
        return _id

    def update_data(self, table, _id, **kwargs):
        """ Update table row with given _id.
        [Input]
            table: string: table name to insert data
            _id: int: row id
            **kwargs: key-value pairs which is <column, value>
        [Return]
            None
        """
        sql = "UPDATE %s SET" % table
        for key in kwargs:
            sql += " %s =" % key
            sql += " %s,"
        sql = sql.rstrip(",") + " WHERE id ="
        sql += " %s"
        vals = kwargs.values()
        lv = list(vals)
        lv.append(_id)
        self._cursor.execute(sql,(lv))
        self._con.commit()

    def stash_data(self, table, **kwargs):
        """ Insert datas into given table without commit.
        [Input]
            table: string: table name to insert data
            **kwargs: key-value pairs which is <column, value>
        [Return]
            None
        """
        sql = "INSERT INTO %s (" % table
        for key in kwargs:
            sql += "%s," % key
        sql = sql.rstrip(",") + ") VALUES ("
        for key in kwargs:
            sql += "%s,"
        sql = sql.rstrip(",") + ")"
        ls = list(kwargs.values())
        try:
            self._cursor.execute(sql, (ls))
        except pymysql.ProgrammingError as e:
            print ("You are probably trying to insert a non-ascii code string.")
            print ("Please check below content:")
            print (kwargs.values())
            raise e
        return self._cursor.lastrowid

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def commit(self):
        self._con.commit()

    def close(self):
        """
        Commit the transcations then close database.
        """
        self._con.commit()
        self._con.close()


def get_projects():
    projects = []
    with RevisionDatabase() as db:
        db._cursor.execute("select * from project")
        for row in db._cursor.fetchall():
            projects.append(dict(row))
    log.debug(projects)
    return projects


def sql_query(sql):
    results = []
    log.debug('start sql_query')
    try:
        with RevisionDatabase() as db:
            db._cursor.execute(sql)
            for row in db._cursor.fetchall():
                results.append(dict(row))
    except Exception as e:
        log.debug('error:', str(e))
    finally:
        log.debug(results)
    return results


def update_rule(rid, column, new_value, user=None):
    # Update rule table's row by id
    # Return the updated column and it's new value
    results = {}
    if isinstance(new_value, bool):
        new_value = int(new_value)
    log.debug(
        "Start update rule %s (column: %s value: %s)" %
        (rid, column, new_value))
    update_user = ""
    if user is None:
        user = getpass.getuser()
    user = user.lower()
    if column == "done":
        update_user = ",editor='%s' " % user
        results["editor"] = user
    elif column == "sc_done":
        update_user = ",sc_editor='%s' " % user
        results["sc_editor"] = user
    elif column == "qa":
        update_user = ",qa_editor='%s' " % user
        results["qa_editor"] = user
    elif column == "sc_qa":
        update_user = ",sc_qa_editor='%s' " % user
        results["sc_qa_editor"] = user
    elif column == "review":
        update_user = ",reviewer='%s' " % user
        results["reviewer"] = user
    else:
        update_user = ""
    with RevisionDatabase() as db:
        log.debug("update rule set {column}=%s {user} where id=%s".format(
            column=column, user=update_user), (new_value, rid))
        db._cursor.execute(
            "update rule set {column}=%s {user} where id=%s".format(
                column=column, user=update_user), (new_value, rid))
    results[column] = new_value
    log.info("Finish update rule")
    return results


def create_project(name, node, due_date):
    log.info("%s %s %s" % (name, node, due_date))
    try:
        due_date = datetime.date.fromtimestamp(due_date / 1000.0)
        due_date = due_date.strftime("%Y-%m-%d")
        pid = 0
        with RevisionDatabase() as db:
            db._cursor.execute(
                "INSERT INTO project (name, node, due_date) VALUES (%s,%s,%s)",
                ([name, node, due_date]))
            pid = db._cursor.lastrowid
    except Exception as e:
        log.error(e)
    return pid


def report_rules(report):
    if re.match(r"^.*\.CPreport_2$", basename(report)):
        parser = DrmDiffReportParser(report)
    else:
        parser = DrmDiffReportParser2(report)
    while True:
        rule = parser.next_rule()
        if rule is None:
            return
        yield rule


def pickle_rules(report):
    assert isinstance(report, DrmDiff), "report must be DrmDiff"
    diff_rules = [x for x in report.diff_rules if x.stat is not DiffStat.STAT_SAME]
    return [Rule.from_diff(x) for x in diff_rules]


def rule_duplicate(rule, old=None):
    if old is None:
        return False
    if rule.name != old['name']:
        return False
    if rule.rule_type != old['rule_type']:
        return False
    if rule.description != old['description']:
        return False
    return True


def is_pickle(report):
    """ Tell if report is .pkl file
    [Input]
        report
    [Return]
        bolean
    """
    name, ext = splitext(report)
    return ext == ".pkl"


def import_report_to_database(db, report, due_date, project,
                              diff_revision=None):
    """ insert new diff report to given database
    [Input]
        db: SqlDatabase instance
        report: diff report's file path
        due_date: string: in the format of Y-M-D
        project: project id to put report
        diff_revision: revision id to diff with
    [Return]
        echo back message in string
    """
    # if not isinstance(db, SqlDatabase):
    #     raise ValueError("db should be SqlDatabase instance")
    old_revision = {}
    # mailservice = SendMail()
    # mailservice.send_mail()
    if diff_revision is not None:
        db._cursor.execute(
            "select * from rule where revision=%s", [diff_revision])
        for row in db._cursor.fetchall():
            old_revision[row['name']] = row
    cp_report = report
    rules_iter = None
    if is_pickle(report):
        report = pickle.load(open(report, "rb"))
        cp_report = report.report
        if hasattr(report, "der_rep"):
            der_report = report.der_rep
            der_report_name = basename(der_report)
        if hasattr(report, "mtsk_rep"):
            mtsk_report = report.mtsk_rep
            mtsk_report_name = basename(mtsk_report)
        rules_iter = pickle_rules(report)
    else:
        rules_iter = report_rules(report)
    report_name = basename(cp_report)
    revision_id = db.put_data(
        "revision", project=project, report=report_name,
        status="Activate", due_date=due_date)
    rule_count = 0
    for rule in rules_iter:
        if not rule_duplicate(rule, old_revision.get(rule.name, None)):
            db.stash_data(
                "rule", revision=str(revision_id), name=rule.name,
                description=rule.description, rule_type=rule.rule_type)
            rule_count += 1
    db.update_data("revision", str(revision_id), total_rules=rule_count)
    db._con.commit()

    if join(report_path(), report_name) == cp_report:
        return "It's same file..."
    shutil.copy(cp_report, report_path())
    os.chmod(join(report_path(), report_name), 0o775)

    if hasattr(report, "der_rep"):
        if join(report_path(), der_report_name) == der_report:
            return "It's same file..."
        shutil.copy(der_report, report_path())
        os.chmod(join(report_path(), der_report_name), 0o775)

    if hasattr(report, "mtsk_rep"):
        if join(report_path(), mtsk_report_name) == mtsk_report:
            return "It's same file..."
        shutil.copy(mtsk_report, report_path())
        os.chmod(join(report_path(), mtsk_report_name), 0o775)

    return "ok"


def import_report(report, due_date, project, diff_revision=None):
    """ Interface for remote query, usually from javascript.
    [Input]
        report: string: diff report's file path
        due_date: time stam in milisecond format. (used in javascript)
        proejct: project id to put report
        diff_revision: revision id to diff with
    [Return]
        string, echo back message
    """
    with RevisionDatabase() as db:
        due_date = datetime.date.fromtimestamp(due_date / 1000.0)
        due_date = due_date.strftime("%Y-%m-%d")
        result = import_report_to_database(
            db, report, due_date, str(project),
            diff_revision=diff_revision)
    return result


def download_excel(sc_condition, target, id):
    columns = ["Rule Name", "Description", "Rule Type", "Owner", "Editor",
               "Done", "QA Editor", "QA", "2nd Owner", "2nd Done",
               "Second QA Editor", "Second QA", "Reviewer", "Review", "Note"]
    table_columns = ["name", "description", "rule_type", "owner", "editor",
                     "done", "qa_editor", "qa", "sc_owner", "sc_done",
                     "sc_qa_editor", "sc_qa", "reviewer", "review", "note"]
    book = xlwt.Workbook()
    sh = book.add_sheet("revision")
    report = "revision.report"
    for col, name in enumerate(columns):
        sh.write(0, col, name)
    with RevisionDatabase() as db:
        db._cursor.execute(
            "select * from rule {}".format(sc_condition))
        row_num = 0
        for row in db._cursor.fetchall():
            row_num += 1
            for col, name in enumerate(table_columns):
                if name == "done":
                    done = ""
                    if row[name] == 1:
                        done = "Coding"
                    if row[name] == 2:
                        done = "Wording"
                    if row[name] == 3:
                        done = "Reject"
                    if row[name] == 4:
                        done = "Reject-Complete"
                    sh.write(row_num, col, done)
                elif name == "sc_done":
                    sc_done = ""
                    if row[name] == 1:
                        sc_done = "Coding"
                    if row[name] == 2:
                        sc_done = "Wording"
                    if row[name] == 3:
                        sc_done = "Reject"
                    if row[name] == 4:
                        sc_done = "Reject-Complete"
                    sh.write(row_num, col, sc_done)
                else:
                    sh.write(row_num, col, row[name])
                    continue
        db._cursor.execute(
            "select report from revision where id=%s", [id])
        report = db._cursor.fetchone()['report']
    (rep_name, ext) = splitext(basename(report))
    book.save(join(target, rep_name + ".xls"))


def open_report(report_name, rule_name):
    report = join(report_path(), report_name)
    if not isfile(report):
        raise Exception("Cannot find {}, Please copy it to {}".format(
            report_name, report_path()))
    os.system(
        "grep -m 1 -n -e '%s' %s | cut -f 1 -d : "
        "| xargs -n 1 -I {} gvim '+{}' %s"
        % (rule_name, report, report))
    return "ok"


def check_all(column, sc_condition, enable_checkall, user=None):
    results = {}
    update_user = ""
    if user is None:
        user = getpass.getuser()
    if enable_checkall == 0:
        user = ""
    user = user.lower()
    if column == "qa":
        update_user = ",qa_editor='%s' " % user
        results["qa_editor"] = user
    elif column == "sc_qa":
        update_user = ",sc_qa_editor='%s' " % user
        results["sc_qa_editor"] = user
    elif column == "review":
        update_user = ",reviewer='%s' " % user
        results["reviewer"] = user
    else:
        update_user = ""
    with RevisionDatabase() as db:
        log.debug("update rule set {}={} {} {} and done=1".format(
            column, enable_checkall, update_user, sc_condition))
        db._cursor.execute(
            "update rule set {}={} {} {} and done=1".format(
                column, enable_checkall, update_user, sc_condition))
