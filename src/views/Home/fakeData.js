export const doneEnum = {
  0: "",
  1: "complete",
  2: "reject",
  3: "coding",
  4: "suck my dick",
};
export const doneOptions = [
  { text: "", value: 0 },
  { text: "complete", value: 1 },
  { text: "reject", value: 2 },
  { text: "coding", value: 3 },
  { text: "suck my dick", value: 4 },
];

export const RuleTableHeader = [
  {
    text: "名稱",
    value: "name",
  },
  {
    text: "rule_type",
    value: "rule_type",
  },
  {
    text: "owner",
    value: "owner",
  },
  {
    text: "editor",
    value: "editor",
  },
  {
    text: "done",
    value: "done",
  },
  {
    text: "qa",
    value: "qa",
  },
  {
    text: "review",
    value: "review",
  },
  {
    text: "sc_qa",
    value: "sc_qa",
  },
  {
    text: "note",
    value: "note",
  },
];

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
