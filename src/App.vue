<template>
  <v-app>
    <v-main>
      <v-card style="height: 100%; padding: 16px">
        <router-view></router-view>
      </v-card>
    </v-main>
    <navigation />
  </v-app>
</template>

<script>
import Navigation from "@/components/feature/navigation/navigation";

export default {
  name: "App",
  components: {
    [Navigation.name]: Navigation,
  },
  data: () => ({
    group: null,
    tree: [],
    filters: {
      keyWord: "",
      date: "",
    },
  }),
  computed: {
    tabs() {
      return []; // this.revisions.filter((x) => x.visible);
    },
  },
  methods: {},
  created() {},
};
</script>

<style lang="scss">
/* width */
::-webkit-scrollbar {
  width: 8px;
}
/* Track */
::-webkit-scrollbar-track {
  border-radius: 10px;
  background: #eee;
}
/* Handle */
::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 10px;
}
/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style>
