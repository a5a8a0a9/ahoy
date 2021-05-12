<template>
  <div>
    <v-navigation-drawer
      app
      fixed
      absolute
      permanent
      hide-overlay
      expand-on-hover
      :mini-variant.sync="mini"
    >
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img
              src="https://randomuser.me/api/portraits/women/85.jpg"
            ></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item link>
          <v-list-item-content>
            <v-list-item-title class="title"> Sandra Adams </v-list-item-title>
            <v-list-item-subtitle>sandra_a88@gmail.com</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>
      <v-list nav dense>
        <v-subheader>Projects</v-subheader>
        <v-list-group
          v-for="(node, nodeIndex) in nodes"
          :key="nodeIndex"
          :value="true"
          prepend-icon="mdi-account-circle"
        >
          <template v-slot:activator>
            <v-list-item-title>{{ node.name }}</v-list-item-title>
          </template>

          <v-list-group
            v-for="(project, projectIndex) in node.projects"
            :key="projectIndex"
            :value="true"
            no-action
            sub-group
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ project.name }}</v-list-item-title>
              </v-list-item-content>
            </template>

            <v-list-item
              v-for="(revision, revisionIndex) in project.revisions"
              link
              :key="revisionIndex"
              active-class="primary-text"
              @click="selectItem(revision)"
            >
              <v-list-item-title v-text="revision.report"></v-list-item-title>

              <v-list-item-icon>
                <v-icon>
                  {{ revision.visible ? "mdi-eye" : "mdi-eye-off" }}
                </v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-list-group>
        </v-list-group>
      </v-list>

      <!-- <v-list nav dense>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Files</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Shared with me</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-star</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Starred</v-list-item-title>
        </v-list-item>
      </v-list> -->
    </v-navigation-drawer>
    <!-- <v-app-bar app color="primary" dark>
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
        <v-subheader>Projects</v-subheader>
        <v-list-group
          v-for="(node, nodeIndex) in nodes"
          :key="nodeIndex"
          :value="true"
          prepend-icon="mdi-account-circle"
        >
          <template v-slot:activator>
            <v-list-item-title>{{ node.name }}</v-list-item-title>
          </template>

          <v-list-group
            v-for="(project, projectIndex) in node.projects"
            :key="projectIndex"
            :value="true"
            no-action
            sub-group
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ project.name }}</v-list-item-title>
              </v-list-item-content>
            </template>

            <v-list-item
              v-for="(revision, revisionIndex) in project.revisions"
              link
              :key="revisionIndex"
              active-class="primary-text"
              @click="selectItem(revision)"
            >
              <v-list-item-title v-text="revision.report"></v-list-item-title>

              <v-list-item-icon>
                <v-icon>
                  {{ revision.visible ? "mdi-eye" : "mdi-eye-off" }}
                </v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-list-group>
        </v-list-group>
      </v-list>
    </v-navigation-drawer> -->
  </div>
</template>

<script>
import { fakeNodeData } from "./fakeData";
export default {
  name: "navigation",
  props: {
    drawer: Boolean,
  },
  data() {
    return {
      mini: false,
      selected: [],
      nodes: [],
    };
  },
  computed: {
    revisionList() {
      return this.nodes.flatMap((node) => {
        return node.projects.flatMap((project) => {
          return project.revisions.filter((revision) => revision.visible);
        });
      });
    },
  },
  methods: {
    getData() {
      fakeNodeData.forEach((node) => {
        if (!node.projects) node.projects = [];
        node.projects.forEach((project) => {
          project.revisions = project.revisions
            ? project.revisions.map((revision) => {
                return { ...revision, visible: false };
              })
            : [];
        });
      });
      this.nodes = fakeNodeData;
    },
    selectItem(revision) {
      revision.visible = !revision.visible;
      this.$store.dispatch("revision/setRevision", revision);
    },
  },
  created() {
    this.getData();
    console.log(this.nodes);
  },
};
</script>
