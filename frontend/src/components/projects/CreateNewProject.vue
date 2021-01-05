<template>
  <v-row>
      <v-col cols="12" md="12" align-self="center">
        <v-text-field
          label="Project Name"
          placeholder="200"
          v-model="name"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="12" align-self="center">
        <v-text-field
          label="Project Description"
          placeholder="200"
          v-model="description"
        ></v-text-field>
      </v-col>
    </v-row>
</template>