<template>
  <div class="home">
    <template v-if="revisionList.length > 0">
      <v-tabs v-model="activeTab" @change="onTabChange($event)">
        <v-tab v-for="revision in revisionList" :key="revision.id">
          <template>
            <span class="text-truncate">
              {{ revision.report }}
            </span>
          </template>
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="activeTab" style="height: 100%">
        <v-tab-item
          v-for="revision in revisionList"
          :key="revision.id"
          style="
            height: 100%;
            display: grid;
            grid-template-rows: max-content max-content 1fr max-content;
          "
        >
          <h4>{{ revision.report }}</h4>
          <v-card flat outlined tile @mouseleave="onMouseleave()">
            <v-toolbar dense>
              <!-- <v-app-bar-nav-icon></v-app-bar-nav-icon> -->
              <!-- <v-toolbar-title>{{ revision.report }}</v-toolbar-title> -->
              <v-spacer></v-spacer>
              <v-btn icon>
                <v-icon>mdi-download</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon>mdi-cog</v-icon>
              </v-btn>
              <v-btn icon @click="toggle()" @mouseenter="onMouseenter()">
                <v-icon :color="filterLock ? 'primary' : 'default'">{{
                  filterLock ? "mdi-lock" : "mdi-lock-open"
                }}</v-icon>
              </v-btn>
            </v-toolbar>
            <v-card-text>
              <v-expand-transition>
                <v-row
                  v-show="isFilterOpen || filterLock"
                  class="filter-content"
                >
                  <v-col cols="3" style="display: flex">
                    <v-text-field
                      v-model="RuleTableFilters.name"
                      :label="RuleTableFilterColumnList.name.label"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="9" style="display: flex">
                    <v-text-field
                      v-model="RuleTableFilters.description"
                      :label="RuleTableFilterColumnList.description.label"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-expand-transition>
              <div
                style="
                  text-align: right;
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                "
              >
                <label class="font-weight-black">filter options:</label>
                <div>
                  <v-btn color="error">
                    <v-icon left> mdi-refresh </v-icon>
                    clear
                  </v-btn>
                  <v-fade-transition>
                    <v-btn color="normal" v-if="isFilterOpen || filterLock">
                      <v-icon left> mdi-magnify </v-icon>
                      search
                    </v-btn>
                  </v-fade-transition>
                </div>
              </div>
            </v-card-text>
          </v-card>
          <v-card flat outlined tile>
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th
                      class="text-left"
                      v-for="header in RuleTableHeader"
                      :key="header.value"
                    >
                      {{ header.text }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="rule in tableData" :key="rule.id">
                    <td v-for="header in RuleTableHeader" :key="header.value">
                      <template
                        v-if="['qa', 'sc_qa', 'review'].includes(header.value)"
                      >
                        <v-checkbox
                          v-if="header.value === 'qa'"
                          v-model="rule.qa"
                          :label="rule.qa_editor"
                          @change="onDataChange(rule)"
                        ></v-checkbox>
                        <v-checkbox
                          v-if="header.value === 'sc_qa'"
                          v-model="rule.sc_qa"
                          :label="rule.sc_qa_editor"
                          @change="onDataChange(rule)"
                        ></v-checkbox>
                        <v-checkbox
                          v-if="header.value === 'review'"
                          v-model="rule.review"
                          :label="rule.reviewer"
                          @change="onDataChange(rule)"
                        ></v-checkbox>
                      </template>
                      <template v-else-if="header.value === 'done'">
                        <v-select
                          style="width: 180px; margin-top: 16px"
                          :items="doneOptions"
                          v-model="rule.done"
                          dense
                          solo
                          @change="onDataChange(rule)"
                        ></v-select>
                      </template>
                      <span v-else @click="copytext(rule[header.value])" ref="">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <span
                              v-bind="attrs"
                              v-on="on"
                              style="cursor: pointer"
                            >
                              {{ rule[header.value] }}
                              <!-- <v-icon large color="blue-grey darken-2"
                                >mdi-call-split</v-icon
                              > -->
                            </span>
                          </template>
                          <span>{{ rule[header.value] }}</span>
                        </v-tooltip>
                      </span>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card>
          <v-pagination
            circle
            v-model="tableSetting.page"
            :length="tableSetting.totalAmount"
            :total-visible="tableSetting.totalVisible"
            @input="onPageChange()"
            @next="onPageChange()"
            @previous="onPageChange()"
          ></v-pagination>
        </v-tab-item>
      </v-tabs-items>
    </template>
    <template v-else>
      <h1>暫無資料</h1>
    </template>

    <v-dialog v-model="dialog" persistent max-width="400">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">
          Open Dialog
        </v-btn>
      </template>
      <v-card v-if="dialogStep === 1">
        <v-card-title class="headline">Upload</v-card-title>
        <v-card-text>
          <p>content 1</p>
          <!-- <input type="file" @change="onFileUpload" /> -->
          <v-file-input
            truncate-length="15"
            placeholder="suck my dick"
            @change="onFileUpload"
          ></v-file-input>
          <!-- <v-btn color="green" @click="dialogStep1Action(200)">success</v-btn>
          <v-btn color="error" @click="dialogStep1Action(400)">fail</v-btn> -->
          <div style="color: red" v-if="errMsg">{{ errMsg }}</div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">
            cancel
          </v-btn>
          <v-btn color="green darken-1" text @click="dialogStep1Action(200)">
            Upload
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card v-else-if="dialogStep === 2">
        <v-card-title class="headline">Upload Success</v-card-title>
        <v-card-text>
          <v-text-field
            label="Next Stage Owner"
            placeholder="Fill in owner"
            v-model="dialogStep2Owner"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialogStep = 1">
            NO
          </v-btn>
          <v-btn color="green darken-1" text @click="dialogStep2Action()">
            YES
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card v-else>
        <v-card-title class="headline">{{ "QC & Archive Stage" }}</v-card-title>
        <v-card-text> {{ successMsg }} </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialogStep = 2">
            Disagree
          </v-btn>
          <v-btn color="green darken-1" text @click="dialogStep3Action()">
            Agree
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { FakeRuleData } from "./fakeData";
import {
  RuleTableHeader,
  doneEnum,
  doneOptions,
  RuleTableFilterColumnList,
} from "./Columns";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      RuleTableFilterColumnList,
      RuleTableFilters: {
        name: "",
        description: "",
        owner: "",
        editor: "",
        qa_editor: "",
        sc_qa_editor: "",
        reviewer: "",
        rule_type: "",
        status: "",
      },
      filterLock: false,
      isFilterOpen: false,
      RuleTableHeader: RuleTableHeader,
      FakeRuleData: FakeRuleData,
      doneEnum: doneEnum,
      doneOptions: doneOptions,
      activeTab: null,
      activeRevisionId: null,
      tableSetting: {
        page: 1,
        itemsPerPage: 5,
        totalVisible: 5,
        totalAmount: Math.ceil(FakeRuleData.length / 5),
      },
      tableData: [],
      dialog: false,
      dialogStep: 1,
      dialogStep2Owner: "",
      errMsg: "",
      successMsg: "",
    };
  },
  computed: {
    ...mapGetters({
      revisionList: "revision/activeTabList",
    }),
  },
  methods: {
    onMouseenter() {
      this.isFilterOpen = true;
    },
    onMouseleave() {
      this.isFilterOpen = false;
    },
    toggle() {
      this.filterLock = !this.filterLock;
    },
    onQaChange(item) {
      item.qa_editor = "王溪明";
    },
    getRuleData(revisionId, page) {
      this.tableData = this.FakeRuleData.slice(
        (page - 1) * this.tableSetting.itemsPerPage,
        page * this.tableSetting.itemsPerPage
      );
    },
    onTabChange(index) {
      this.activeRevisionId = this.revisionList[index].id;
      this.tableSetting.page = 1;
      this.onPageChange();
    },
    onPageChange() {
      this.getRuleData(this.activeRevisionId, this.tableSetting.page);
    },
    onDataChange(rowData) {
      console.log(rowData);
      // this.loading = true;

      // this.axios({
      //   url: `${base}/api/rules/${this.activeRevisionId}`,
      //   method: "post",
      //   data: {
      //     ...rowData,
      //   },
      // })
      //   .then((response) => {
      //     console.log(response);
      //   })
      //   .finally(() => {});
    },
    copytext(text) {
      var oInput = document.createElement("input");
      oInput.value = text; //賦值
      document.body.appendChild(oInput);
      oInput.select(); // 選擇物件
      document.execCommand("Copy"); // 執行瀏覽器複製命令
      oInput.style.display = "none";
      alert(`已複製${text}`);
    },
    /**---------------------------------------------------------------- */
    onFileUpload(event) {
      console.log(event);
    },
    dialogStep1Action(input) {
      this.upload1(input)
        .then(() => {
          this.errMsg = "";
          this.dialogStep = 2;
        })
        .catch((e) => {
          this.errMsg = e.description;
        });
    },
    dialogStep2Action() {
      console.log(this.dialogStep2Owner);
      this.upload2(this.dialogStep2Owner).then((response) => {
        this.successMsg = response;
        this.dialogStep = 3;
      });
    },
    dialogStep3Action() {
      this.dialog = false;
    },
    upload1(status) {
      return new Promise((resolve, reject) => {
        if (status === 200) {
          resolve({
            status: "success",
            description: "success",
          });
        } else {
          reject({
            status: "fail",
            description:
              "Cannot find product with given name and version (1 2).",
          });
        }
      });
    },
    upload2(owner) {
      return new Promise((resolve) => {
        resolve(`${owner} success`);
      });
    },
  },
  mounted() {},
};
</script>

<style lang="scss" scoped>
.home {
  display: grid;
  grid-template-rows: max-content 1fr;
}

::v-deep .v-tabs-slider-wrapper {
  width: 250px !important;
}

::v-deep .v-pagination {
  justify-content: flex-end;
}
.v-tab {
  width: 250px;
}
.filter {
  &-content {
    transition: all 0.5s;
    margin: unset;
    padding: 12px;
  }
}

.v-data-table {
  height: 100%;
}
::v-deep .v-data-table__wrapper {
  height: 100%;
}
</style>
