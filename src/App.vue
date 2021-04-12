<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-card style="height: 100%; padding: 16px">
        <router-view></router-view>
      </v-card>
    </v-main>
    <navigation :drawer="drawer" />
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
    drawer: false,
    group: null,
  }),
  methods: {},
  computed: {
    tabs() {
      return []; // this.revisions.filter((x) => x.visible);
    },
  },
};
</script>
