<template>
  <div class="home">
    <template v-if="revisionList.length > 0">
      <v-tabs v-model="activeTab" @change="onTabChange($event)">
        <v-tab v-for="revision in revisionList" :key="revision.id">
          {{ revision.report }}
        </v-tab>
      </v-tabs>

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
                      ></v-checkbox>
                      <v-checkbox
                        v-if="header.value === 'sc_qa'"
                        v-model="rule.sc_qa"
                        :label="rule.sc_qa_editor"
                      ></v-checkbox>
                      <v-checkbox
                        v-if="header.value === 'review'"
                        v-model="rule.review"
                        :label="rule.reviewer"
                      ></v-checkbox>
                    </template>
                    <template v-else-if="header.value === 'done'">
                      <v-select
                        :items="doneOptions"
                        v-model="rule.done"
                        dense
                        solo
                      ></v-select>
                    </template>
                    <span v-else>{{ rule[header.value] }}</span>
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
import {
  RuleTableHeader,
  FakeRuleData,
  doneEnum,
  doneOptions,
} from "./fakeData";

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
  },
  mounted() {},
};
</script>

<style lang="scss" scoped>
.v-tabs:not(.v-tabs--vertical) .v-tab {
  display: inline-block;
  white-space: nowrap;
  word-break: keep-all;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-top: 1rem;
  max-width: 150px;
}

::v-deep .v-tabs-slider-wraper {
  width: 150px;
}
</style>
