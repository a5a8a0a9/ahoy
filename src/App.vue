<template>
  <v-app>
    <navigation :drawer="drawer" />
    <v-app-bar color="primary" dark app></v-app-bar>

    <v-main>
      <v-container fluid style="height: 100%">
        <router-view></router-view>
      </v-container>
    </v-main>
    <!-- <v-main>
      <v-card style="height: 100%; padding: 16px">
        <router-view></router-view>
      </v-card>
    </v-main>
    <navigation /> -->
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
      drawer: true,
      group: null,
      tree: [],
      filters: {
        keyWord: "",
        date: "",
      },
    };
  },
  computed: {
    tabs() {
      return []; // this.revisions.filter((x) => x.visible);
    },
  },
  methods: {},
  created() {},
};
</script>

<style lang="scss" scoped>
::v-deep .container > div {
  height: 100%;
}
</style>
