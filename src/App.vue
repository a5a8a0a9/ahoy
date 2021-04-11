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
        <home :tabs="tabs" />
      </v-card>
    </v-main>

    <v-navigation-drawer
      v-model="drawer"
      app
      absolute
      clipped
      :mini-variant.sync="mini"
      fixed
      hide-overlay
    >
      <v-list nav dense>
        <v-list-group
          prepend-icon="mdi-menu"
          v-for="project in projects"
          :key="project.title"
        >
          <template v-slot:activator>
            <v-list-item-title>{{ project.title }}</v-list-item-title>
          </template>
          <v-list-item-group
            v-model="selected"
            active-class="primary--text"
            multiple
          >
            <template v-for="(revision, index) in project.revisions">
              <v-list-item
                :key="revision.title"
                @click="revision.visible = !revision.visible"
              >
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      v-text="revision.title"
                    ></v-list-item-title>

                    <v-list-item-subtitle>
                      <template>
                        <v-progress-linear
                          :value="revision.progress"
                        ></v-progress-linear>
                      </template>
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action>
                    <v-list-item-action-text
                      v-text="`${revision.progress}%`"
                    ></v-list-item-action-text>

                    <v-icon
                      :color="
                        revision.visible ? 'primary darken-3' : 'grey lighten-1'
                      "
                    >
                      {{ revision.visible ? "mdi-eye" : "mdi-eye-off" }}
                    </v-icon>
                  </v-list-item-action>
                </template>
              </v-list-item>

              <v-divider
                v-if="index < project.revisions.length - 1"
                :key="index"
              ></v-divider>
            </template>
          </v-list-item-group>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
  </v-app>
</template>

<script>
import Home from "./views/Home";

export default {
  name: "App",
  components: {
    Home,
  },
  data: () => ({
    drawer: false,
    mini: false,
    group: null,
    selected: [],
    projects: [],
  }),
  methods: {
    getData() {
      for (let i = 0; i < 10; i++) {
        this.projects.push({
          title: `project-${i}`,
          revisions: [
            {
              title: `revision-1`,
              progress: i * 10,
              visible: false,
            },
            {
              title: `revision-2`,
              progress: i * 10,
              visible: false,
            },
            {
              title: `revision-3`,
              progress: i * 10,
              visible: false,
            },
          ],
        });
      }
    },
  },
  computed: {
    tabs() {
      return []; // this.revisions.filter((x) => x.visible);
    },
  },
  created() {
    this.getData();
  },
};
</script>
