<template>
  <div class="home">
    <template v-if="revisionList.length > 0">
      <v-tabs v-model="activeTab" @change="onTabChange($event)">
        <v-tab v-for="revision in revisionList" :key="revision.id">
          {{ revision.report }}
        </v-tab>
      </v-tabs>

      <!-- <div class="flex-tabs">
        <div class="flex-tab" v-for="revision in revisionList" :key="revision.id"></div>
      </div> -->

      <v-tabs-items v-model="activeTab">
        <v-tab-item v-for="revision in revisionList" :key="revision.id">
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
          <v-pagination
            v-model="tableSetting.page"
            :length="tableSetting.totalAmount"
            :total-visible="tableSetting.totalVisible"
            @input="onPageChange()"
            @next="onPageChange()"
            @previous="onPageChange()"
          ></v-pagination>

          <!-- <v-data-table
            :headers="RuleTableHeader"
            :items="FakeRuleData"
            class="elevation-1"
          >
            <template v-slot:[`item.qa`]="{ item }">
              <v-checkbox
                v-model="item.qa"
                :label="item.qa_editor"
                @change="onQaChange(item)"
              ></v-checkbox>
            </template>
            <template v-slot:[`item.sc_qa`]="{ item }">
              <v-checkbox
                v-model="item.sc_qa"
                :label="item.sc_qa_editor"
              ></v-checkbox>
            </template>
            <template v-slot:[`item.review`]="{ item }">
              <v-checkbox
                v-model="item.review"
                :label="item.reviewer"
              ></v-checkbox>
            </template>
          </v-data-table> -->
        </v-tab-item>
      </v-tabs-items>
    </template>
    <template v-else>
      <h1>暫無資料</h1>
    </template>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { FakeRuleData } from "./fakeData";
import { RuleTableHeader, doneEnum, doneOptions } from "./Columns";

export default {
  name: "Home",
  components: {},
  data() {
    return {
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
    };
  },
  computed: {
    ...mapGetters({
      revisionList: "revision/activeTabList",
    }),
  },
  methods: {
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
      //   method: 'post',
      //   data: rowData
      // }).then(response => {
      //   console.log(response)
      // }).finally(() => {})
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
  },
  mounted() {},
};
</script>

<style lang="scss" scoped>
// .v-tabs:not(.v-tabs--vertical) .v-tab {
//   display: inline-block;
//   white-space: nowrap;
//   word-break: keep-all;
//   overflow: hidden;
//   text-overflow: ellipsis;
//   padding-top: 1rem;
//   max-width: 150px;
// }

// ::v-deep .v-tabs-slider-wraper {
//   width: 150px;
// }

.flex-tabs {
  display: flex;
  align-items: center;
  justify-content: stretch;
}
</style>
