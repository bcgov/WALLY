<template>
    <v-card>
      <v-card-title class="headline">
        Edit monthly allocation values
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="exit"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>Nam dictum fringilla velit et placerat. Aliquam ultricies massa gravida posuere ullamcorper. Duis fermentum purus felis. Duis fermentum lectus vel purus accumsan consectetur. Nunc suscipit mauris a eleifend consectetur. Vestibulum at odio lorem. Integer vel dignissim purus, nec pretium mi.</v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="alloc-item">Name</th>
            <th scope="col" class="text-left alloc-value" v-for="month in months" :key="month">{{month}}</th>
            <th scope="col"></th>
          </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in allocItems" :key="`${i}-${item.name}`">
              <td>{{item.name}}</td>
              <td v-for="(month, j) in months" :key="`${j}-${month}`">
                <v-text-field
                  class="alloc-value"
                  suffix="/12"
                  dense
                  filled
                  v-model="item.values[j]"
                  hide-details="auto"
                  color="primary"
                >
                </v-text-field>
              <p class="font-weight-light caption text-right">
                {{computeDecimal(item.values[j]) | formatNumber}}
              </p>
              </td>
            <td>
              <v-chip small :color="(computeRowTotal(item.values) === 12)?'green': 'red'">
                <v-avatar left
                >
                  <v-icon small v-if="computeRowTotal(item.values) === 12">mdi-check</v-icon>
                  <v-icon small v-else>mdi-close</v-icon>
                </v-avatar>
                {{computeRowTotal(item.values)}}
              </v-chip>
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary lighten-1" depressed @click="saveValues">Apply</v-btn>
        <v-btn color="grey" dark depressed @click="exit">Cancel</v-btn>
      </v-card-actions>
    </v-card>
</template>
<style lang="scss">
  .alloc-item{
    width: 300px;
  }
  .alloc-value{
    width: 70px;
  }
  .v-text-field__suffix{
    font-size: smaller;
    opacity: 0.2;
  }
  .v-text-field{
    input {
      text-align: right;
    }
  }
  .v-data-table {
    td {
      padding: 0 2px;
    }

    td.purpose-type {
      padding: 0 15px;
    }

    td:last-child{
      padding: 0 15px;
    }

  }
</style>
<script src="./MonthlyAllocationTable.js"/>
