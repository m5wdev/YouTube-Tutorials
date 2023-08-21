<template>
  <div>
    <dropzone
      v-if="drop"
      @vdropzone-file-added="onFileAdded"
      @vdropzone-removed-file="removeFileOne"
      @vdropzone-error="onError"
      @vdropzone-success="onSuccess"
      @vdropzone-complete="onComplete"
      @vdropzone-max-files-reached="MaxFile"
      @vdropzone-thumbnail="Onthumbnail"
      ref="DropLabel"
      id="dropzone"
      :options="dropzoneOptions"
    />
  </div>
</template>

<script>
export default {
  props: [
    "photo_label",
    "urlRemovePhoto",
    "urlAddPhoto",
    "paramname",
    "Submit",
    "autoProcessQueue",
    "AddPhoto"
  ],
  mounted() {
    if (!process.client) return;
    this.drop = true;
    let self = this;
    if (self.photo_label) {
      this.image_name = self.photo_label;
      this.dropzoneOptions.init = function () {
        var thisDropzone = this;
        var mockFile = { name: self.photo_label, size: 12, type: "image/jpeg" };
        thisDropzone.emit("addedfile", mockFile);
        thisDropzone.emit("success", mockFile);
        thisDropzone.emit("thumbnail", mockFile, self.photo_label);
        setTimeout(() => {
          self.MaxFile(mockFile);
          try {
            document.querySelector(".dz-remove").innerHTML = "удалить";
          } catch (error) {}
        }, 1000);
      };
    }
  },
  data() {
    return {
      drop: false,
      image_name: null,
      document: false,
      url: this.urlAddPhoto,
      dropzoneOptions: {
        url: this.urlAddPhoto,
        autoProcessQueue: this.autoProcessQueue,
        method: "post",
        paramName: this.paramname,
        maxFiles: 1,
        thumbnailWidth: 260,
        thumbnailHeight: 260,
        resizeWidth: 3000,
        resizeHeight: 2500,
        resizeQuality: 0.5,
        resizeMimeType: "image/jpeg",
        thumbnailMethod: "contain",
        addRemoveLinks: true,
        parallelUploads: 1,
        timeout: 120000,
        dictMaxFilesExceeded: "Достигнут лимит загрузки файлов, разрешено ",
        dictDefaultMessage:
          '<div class="dz-message">Нажмите или перетащите сюда файл для загрузки </div>',
        acceptedFiles: "image/*",
      },
    };
  },
  watch: {
    Submit(newValue, oldValue) {
      if (newValue) {
        this.dropzoneOptions.url = this.urlAddPhoto;

        this.$refs.DropLabel.processQueue();
      }
    },
  },
  computed: {},
  methods: {
    MaxFile(file) {
      this.$refs.DropLabel.removeEventListeners();
      console.log("max-file");
    },
    Onthumbnail(file, dataUrl) {
      console.log();
    },
    removeFileOne(e) {
      this.$refs.DropLabel.setupEventListeners();
      if (this.photo_label) {
        this.OnRemoveApi();
      }
    },
    OnRemoveApi() {
      console.log("remove");
      let headers = {
        "Content-Type": "application/json",
      };
      console.log("delete");
      this.$axios
        .$delete(this.urlRemovePhoto, {
          headers: headers,
        })
        .then((resp) => {
          this.photo_label = null;
        });
    },
    onFileAdded(e) {},
    onError(e) {},
    onSuccess(e) {
      this.photo_label = null;
    },
    onComplete(e) {
      document.querySelector(".dz-remove").innerHTML = "удалить";
    },
  },
};
</script>

<style scoped>
.dropzone.dz-clickable {
  cursor: pointer;
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}
.fakedrop {
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border: 1px solid #ededed;
  padding: 1em;
  text-align: center;
}
.fakedrop p {
  color: #777777cc;
}
</style>
