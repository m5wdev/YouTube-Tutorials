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
      ref="DropImages"
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
  props: ["AddImages"],
  mounted() {
    if (!process.client) return;
    this.drop = true;
    let self = this;
    // this.label_photo = this.logo_company;
    // if (self.logo_company) {
    //   this.image_name = self.logo_company;
    //   this.dropzoneOptions.init = function () {
    //     var thisDropzone = this;
    //     var mockFile = { name: self.logo_company, size: 12, type: "image/jpeg" };
    //     self.onFileAdded(mockFile)
    //     thisDropzone.emit("addedfile", mockFile);
    //     thisDropzone.emit("success", mockFile);
    //     thisDropzone.emit("thumbnail", mockFile, self.logo_company);
    //     this.on("maxfilesexceeded", function (file) {
    //       this.removeFile(file);
    //       alert("No more files please!");
    //     });
    //   };
    // }
  },
  data() {
    return {
      drop: false,
      image_name: null,
      document: false,
      label_photo: [],
      maxFiles:false,
      dropzoneOptions: {
        url: `/api/parcel/add-photo/`,
        method: "post",
        paramName: "logo_company",
        maxFiles: 8,
        autoProcessQueue: false,
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
          '<div class="d-flex align-center justify-center"><img class="mr-2" height="25p" src="/uploadimage.png" alt=""><div class="" style="font-size:16px">Перетащите фотографии компании </div></div>',
        acceptedFiles: "image/*",
        //   headers: { "My-Awesome-Header": "header value" }
      },
    };
  },
  computed: {},
  methods: {
    removeFileOne(e) {
        if (this.maxFiles){
    this.$refs.DropImages.setupEventListeners();
    }
      console.log('one');
      this.AddImages(this.$refs.DropImages.dropzone.files);
    },
    MaxFile(file) {
    this.$refs.DropImages.removeEventListeners();
    this.maxFiles = true
      console.log("max-file");
    },

    onFileAdded(e) {

      this.AddImages(this.$refs.DropImages.dropzone.files);
      console.log(12, e.upload.filename);
    },
    onError(e) {},
    onSuccess(e) {},
    onComplete(e) {
      try {
        this.image_name = JSON.parse(e.xhr.response).name;
        this.$store.commit("dataformparcel/Setimage_label", this.image_name);
        document.querySelector(".dz-remove").innerHTML = "удалить";
      } catch (error) {
        console.log("error");
      }
    },
  },
};
</script>
<style>
.dropzone.dz-clickable {
  font-weight: 800;
  border: 2px dotted #e5e5e5;
  background-color: #f9fafb;
  border-radius: 8px !important;
}
</style>
