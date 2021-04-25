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
  methods: {
    getData(input) {
      return new Promise((resolve, reject) => {
        if (input > 1) {
          let data = [1, 2, 3];
          resolve(data);
        } else {
          reject(666);
        }
      });
    },
  },
  created() {
    this.getData(-1).then((data) => {
      console.log(data);
    });
  },
};
</script>
