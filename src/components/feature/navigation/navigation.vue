<template>
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
            @click="selItem(revision)"
          >
            <v-list-item-title v-text="revision.name"></v-list-item-title>

            <v-list-item-icon>
              <v-icon>
                {{ revision.visible ? "mdi-eye" : "mdi-eye-off" }}
              </v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list-group>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
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
      nodes: fakeNodeData,
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
    getData() {},
    selItem(revision) {
      revision.visible = !revision.visible;
      this.$store.dispatch("revision/setRevision", this.revisionList);
    },
  },
  created() {
    this.getData();
  },
};
</script>
