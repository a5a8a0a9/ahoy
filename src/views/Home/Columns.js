export const doneEnum = {
  0: "",
  1: "complete",
  2: "reject",
  3: "coding",
  4: "complete reject",
};

export const doneOptions = [
  { text: "", value: 0 },
  { text: "complete", value: 1 },
  { text: "reject", value: 2 },
  { text: "coding", value: 3 },
  { text: "complete reject", value: 4 },
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

export const RuleTableFilterColumnList = {
  name: {
    label: "name",
    filter: {
      type: "text",
      default: "",
    },
  },
  description: {
    label: "description",
    filter: {
      type: "text",
      default: "",
    },
  },
  owner: {
    label: "owner",
    filter: {
      type: "text",
      default: "",
    },
  },
  editor: {
    label: "editor",
    filter: {
      type: "text",
      default: "",
    },
  },
  qa_editor: {
    label: "qa_editor",
    filter: {
      type: "text",
      default: "",
    },
  },
  sc_qa_editor: {
    label: "sc_qa_editor",
    filter: {
      type: "text",
      default: "",
    },
  },
  reviewer: {
    label: "reviewer",
    filter: {
      type: "text",
      default: "",
    },
  },
  rule_type: {
    label: "rule_type",
    filter: {
      type: "select",
      default: "",
    },
  },
  status: {
    label: "status",
    filter: {
      type: "select",
      default: "",
    },
  },
};
