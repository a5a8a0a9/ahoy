import { doneEnum } from "./Columns";
export const FakeRuleData = Array.from({ length: 10 }, (v, i) => {
  return {
    id: i + 1,
    revision: i + 1,
    name: `rule${i + 1}`,
    description: `description${i + 1}`,
    rule_type: `rule_type${i + 1}`,
    owner: `owner${i + 1}`,
    editor: `editor${i + 1}`,
    done: i % 5,
    doneName: doneEnum[i % 5],
    qa_editor: `qa_editor${i + 1}`,
    qa: true,
    reviewer: `reviewer${i + 1}`,
    review: false,
    sc_qa_editor: `sc_qa_editor${i + 1}`,
    sc_qa: false,
    note: `note${i + 1}`,
    update_date: new Date(),
  };
});

// export const FakeRuleData = [
//   {
//     id: 1,
//     revision: 1,
//     name: "rule1",
//     description: "description1",
//     rule_type: "rule_type1",
//     owner: "owner1",
//     editor: "editor1",
//     done: 0,
//     qa_editor: "qa_editor1",
//     qa: 0,
//     reviewer: "reviewer1",
//     review: 0,
//     sc_qa_editor: "sc_qa_editor1",
//     sc_qa: 0,
//     note: "note1",
//     update_date: new Date(),
//   },
// ];
