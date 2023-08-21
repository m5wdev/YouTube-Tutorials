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
      ref="DropLabel"
      id="dropzone"
      :options="dropzoneOptions"
    />

    <div class="mt-4">
      <p
        style="font-weight: bold;
    color: #666666;
}"
        class="text-center"
      ></p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["logo_company","urlpath","autoProcessQueue", "AddLogo"],
  mounted() {
    if (!process.client) return;
    this.drop = true;
    let self = this;
    this.label_photo = this.logo_company;
    if (self.logo_company) {
      this.image_name = self.logo_company;
      this.dropzoneOptions.init = function () {
        var thisDropzone = this;
        var mockFile = { name: self.logo_company, size: 12, type: "image/jpeg" };
        self.onFileAdded(mockFile)
        thisDropzone.emit("addedfile", mockFile);
        thisDropzone.emit("success", mockFile);
        thisDropzone.emit("thumbnail", mockFile, self.logo_company);
        this.on("maxfilesexceeded", function (file) {
          this.removeFile(file);
          alert("No more files please!");
        });
      };
    }
  },
  data() {
    return {
      drop: false,
      image_name: null,
      document: false,
      label_photo: [],
      dropzoneOptions: {
        url: this.urlpath,
        method: "post",
        paramName: "logo_company",
        maxFiles: 1,
        autoProcessQueue: this.autoProcessQueue,
        thumbnailWidth: 160,
        thumbnailHeight: 160,
        resizeWidth: 1000,
        resizeHeight: 1000,
        resizeQuality: 0.5,
        resizeMimeType: "image/jpeg",
        thumbnailMethod: "contain",
        addRemoveLinks: true,
        parallelUploads: 2,
        timeout: 120000,
        dictMaxFilesExceeded: "Достигнут лимит загрузки файлов, разрешено ",
        dictDefaultMessage:
          '<div class="d-flex align-center justify-center"><img class="mr-2" height="25p" src="/uploadimage.png" alt=""><div class="" style="font-size:16px">Перетащите фотографии </div></div>',
        acceptedFiles: "image/*",
        //   headers: { "My-Awesome-Header": "header value" }
      },
    };
  },
  computed: {},
  methods: {
    removeFileOne(e) {
      this.$refs.DropLabel.setupEventListeners();
      this.AddLogo("");
    },
    MaxFile(file) {
      this.$refs.DropLabel.removeEventListeners();
      console.log("max-file");
    },

    onFileAdded(e) {
        console.log(e);
      this.AddLogo(e);
      // console.log(12,e.upload.filename);
    },
    onError(e) {},
    onSuccess(e) {},
    onComplete(e) {
    },
  },
};
</script>

<style scoped>
.dropzone.dz-clickable {
  cursor: pointer;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border: 2px dotted #e5e5e5;
  background-color: #f9fafb;
  border-radius: 8px !important;
}
.fakedrop {
  min-height: 160px;
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
