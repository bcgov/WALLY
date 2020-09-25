<template>
  <div id="fileDragDrop">
    <form class="drop-files">
      <label class="drop-files" for="file"><v-icon>mdi-cloud-upload</v-icon> Drop the files here, or <a>browse</a>!</label>
      <input type="file" name="files[]" id="file" class="box__file" data-multiple-caption="x files selected" multiple />
    </form>
  </div>
</template>

<script>
import EventBus from '../../services/EventBus'

export default {
  name: 'FileDrop',
  props: [],
  data: () => ({
    files: [],
    dragOver: false,
    insideBox: false
  }),
  methods: {
    setEvents () {
      const dropZone = this.$el.querySelector('form')
      const input = this.$el.querySelector('input[type="file"]')
      // const fileUpload = this.$el.firstElementChild

      const allEvents = ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop']
      const dragEnteredEvents = ['dragover', 'dragenter']
      const dragLeaveEvents = ['dragleave', 'dragend', 'drop']

      allEvents.forEach((event) => {
        dropZone.addEventListener(event, (e) => {
        // preventing the unwanted behaviours
          e.preventDefault()
          e.stopPropagation()
        })
      })

      dragEnteredEvents.forEach((event) => {
        dropZone.addEventListener(event, e => {
          dropZone.classList.add('is-dragover')
        })
      })

      dragLeaveEvents.forEach((event) => {
        dropZone.addEventListener(event, e => {
          dropZone.classList.remove('is-dragover')
        })
      })

      dropZone.addEventListener('drop', (e) => {
        let droppedFiles = e.dataTransfer.files // the files that were dropped

        console.log(droppedFiles)
        // this.showFiles(droppedFiles)
        EventBus.$emit('import:load-files', droppedFiles)

        // triggerFormSubmit();
      })

      input.addEventListener('change', (e) => {
        EventBus.$emit('import:load-files', e.target.files)
      })
    }
  },
  computed: {
  },
  mounted () {
    this.setEvents()
  },
  beforeDestroy () {
  }
}
</script>

<style lang="scss">
#fileDragDrop {
  position: relative;
  height: 300px;

  .drop-files{
    /*float: left;*/
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
  }
  form.drop-files {
    display: block;
    height: 200px;
    width: 400px;
    background: #ccc;
    margin: auto;
    /*margin-top: 40px;*/
    text-align: center;
    line-height: 200px;
    border-radius: 4px;
    outline: 2px dashed #989898;
    outline-offset: -10px;
    -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
    transition: outline-offset .15s ease-in-out, background-color .15s linear;
  }
  span.drop-files{
    /*margin-top: 80px;*/
    /*height: 80px;*/
  }
  .box__file {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }
  form.is-dragover{
    background-color: #88aadd;
    outline: 2px dashed #617ea8;
  }
}
</style>
