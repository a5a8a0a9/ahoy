<template>
  <v-app style="height: 100%">
    <navigation />
    <!-- <v-dialog v-model="dialog" persistent max-width="400">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="default" v-bind="attrs" v-on="on"> Open Dialog </v-btn>
      </template>
      <v-card v-if="dialogStep === 1">
        <v-card-title class="headline">Upload</v-card-title>
        <v-card-text>
          <p>content 1</p>
          <v-file-input
            truncate-length="15"
            placeholder="suck my dick"
            @change="onFileUpload"
          ></v-file-input>
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
    </v-dialog> -->

    <v-main style="background: #eff0f4; height: calc(100% - 64px)">
      <v-container fluid style="height: 100%; padding: 16px">
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Navigation from "@/components/feature/navigation";

export default {
  name: "App",
  components: {
    [Navigation.name]: Navigation,
  },
  data() {
    return {
      group: null,
      tree: [],
      filters: {
        keyWord: "",
        date: "",
      },
      dialog: false,
      dialogStep: 1,
      dialogStep2Owner: "",
      errMsg: "",
      successMsg: "",
    };
  },
  computed: {
    tabs() {
      return [];
    },
  },
  methods: {
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
  created() {},
};
</script>

<style lang="scss" scoped>
::v-deep .container > div {
  height: 100%;
}
</style>
