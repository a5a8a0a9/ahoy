CREATE TABLE node(
    id integer primary key,
    name text
);
CREATE TABLE project(
    id integer primary key,
    name text,
    node INTEGER DEFAULT null,
    create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date text,
    progress REAL DEFAULT 0,
    FOREIGN KEY (node) REFERENCES node(id)
);
CREATE INDEX project_name ON project (name);
CREATE TABLE revision (
    id    INTEGER PRIMARY KEY,
    project INTEGER,
    report    TEXT,
    status    TEXT,
    create_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date  DATETIME,
    finish_rules  INTEGER DEFAULT 0,
    total_rules INTEGER DEFAULT 0,
    update_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project) REFERENCES project(id)
);
CREATE INDEX revision_project ON revision (project);
CREATE INDEX revision_report ON revision (report);
CREATE INDEX revision_status ON revision (status);
CREATE TABLE "rule" (
    id    INTEGER PRIMARY KEY,
    revision    INTEGER,
    name  TEXT,
    description   TEXT,
    rule_type TEXT,
    owner TEXT,
    editor    TEXT,
    done  INTEGER DEFAULT 0,
    qa_editor TEXT,
    qa    INTEGER DEFAULT 0,
    reviewer  TEXT,
    review    INTEGER DEFAULT 0,
    sc_qa_editor  TEXT,
    sc_qa INTEGER DEFAULT 0,
    note  TEXT,
    update_date   DATETIME DEFAULT CURRENT_TIMESTAMP, sc_done INTEGER DEFAULT 0, sc_owner TEXT, sc_editor TEXT,
    FOREIGN KEY (revision) REFERENCES revision(id)
);
CREATE INDEX rule_revision ON rule (revision);
CREATE INDEX rule_name ON rule (name);
CREATE INDEX rule_description ON rule (description);
CREATE INDEX rule_rule_type ON rule (rule_type);
CREATE INDEX rule_editor ON rule (editor);
CREATE INDEX rule_done ON rule (done);
CREATE INDEX rule_qa_editor ON rule (qa_editor);
CREATE INDEX rule_qa ON rule (qa);
CREATE INDEX rule_reviewer ON rule (reviewer);
CREATE INDEX rule_review ON rule (review);
CREATE INDEX rule_sc_qa_editor ON rule (sc_qa_editor);
CREATE INDEX rule_sc_qa ON rule (sc_qa);
CREATE INDEX project_due_date ON project (due_date);
CREATE INDEX revision_due_date ON revision (due_date);
CREATE INDEX rule_sc_done ON rule (sc_done);
CREATE INDEX rule_sc_editor ON rule (sc_editor);
CREATE TRIGGER update_rule_time AFTER UPDATE ON rule FOR EACH ROW BEGIN
    UPDATE rule SET update_date = CURRENT_TIMESTAMP WHERE id = old.id;
    UPDATE revision SET update_time = CURRENT_TIMESTAMP WHERE id = old.revision;
END
CREATE TRIGGER update_revision_time AFTER INSERT ON revision FOR EACH ROW BEGIN
    UPDATE revision SET create_date = CURRENT_TIMESTAMP WHERE id = new.id;
END;
CREATE TRIGGER update_revision_progress AFTER UPDATE ON rule FOR EACH ROW
WHEN new.done != old.done and (new.done <= 0 or old.done <=0) BEGIN
    UPDATE revision SET finish_rules=finish_rules+(
        CASE WHEN new.done > 0 THEN 1 ELSE -1 END)
    WHERE revision.id=old.revision;
END;
CREATE TRIGGER update_project_progress AFTER UPDATE ON revision FOR EACH ROW
WHEN new.finish_rules != old.finish_rules BEGIN
    UPDATE project SET progress=(
        SELECT sum(finish_rules) * 1.0 / max(1, sum(total_rules)) FROM revision
        WHERE project=new.project)
    WHERE id=new.project;
    UPDATE revision SET status=(
        CASE WHEN new.finish_rules=new.total_rules THEN 'Done' ELSE 'Activate' END)
    WHERE revision.id=new.id;
END;
CREATE TRIGGER update_moved_project_progress AFTER UPDATE ON revision FOR EACH ROW
WHEN new.project != old.project BEGIN
    UPDATE project SET progress=(
        SELECT sum(finish_rules) * 1.0 / max(1, sum(total_rules)) FROM revision
        WHERE project=new.project)
    WHERE id=new.project;
    UPDATE project SET progress=(
        SELECT sum(finish_rules) * 1.0 / max(1, sum(total_rules)) FROM revision
        WHERE project=old.project)
    WHERE id=old.project;
END;
CREATE TRIGGER delete_revision AFTER DELETE ON revision FOR EACH ROW
BEGIN
    UPDATE project SET progress=(
        SELECT sum(finish_rules) * 1.0 / max(1, sum(total_rules)) FROM revision
        WHERE project=old.project)
    WHERE id=old.project;
    DELETE FROM rule WHERE revision=old.id;
END;
CREATE TRIGGER delete_proejct AFTER DELETE ON project FOR EACH ROW
BEGIN
    DELETE FROM revision WHERE project=old.id;
END;