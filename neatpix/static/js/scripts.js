
var facebook = {

  socialLoginRoute: '/auth/facebook/',
  SDKSource: '//connect.facebook.net/en_US/sdk.js',
  userFields: 'id,email,first_name,last_name,picture',

  messages: {
    FBLoggingIn: '<i class="fa fa-spinner fa-fw fa-spin"></i> connecting to Facebook...',
    FBLogInFailed: '<i class="fa fa-frown-o fa-fw"></i> Could not log in with Facebook!',
    authLoggingIn: '<i class="fa fa-spinner fa-fw fa-spin"></i> Logging in...'
  },

  appConfig: {
    appId: '199122750434087',
    version: 'v2.5',
    cookie: true
  },
  
  // intializes facebook related features:
  init: function(){
    facebook.initSDK();
    facebook.configUI();
  },

  // loads and initializes the facebook-Javascipt SDK
  initSDK: function(){
    $.ajaxSetup({ cache: true });
    $.getScript(facebook.SDKSource, function(){
        FB.init(facebook.appConfig);
      }
    );
  },

  // gets Jquery selections for the UI elements
  // related with this component.
  configUI: function(){
    facebook.loginButton = $('#facebook-login-action');
    facebook.LoginStatusLabel = $('#facebook-login-status');
    facebook.csrfForm = $('#login-csrf');
    facebook.registerEventHandlers();
  },   

  // bind event listeners to the component
  // UI elements where necessary:
  registerEventHandlers: function(){
    facebook.loginButton.click(facebook.onLoginClicked);
  },

  // event handler for log
  onLoginClicked: function(){
    facebook.LoginStatusLabel.html(facebook.messages.FBLoggingIn);
    FB.login(
      facebook.onFBLoginResponse,
      {scope: 'email,user_likes'}
    );
    facebook.authLogin();
  },

  // process the facebook login response
  onFBLoginResponse: function(response){
    if (response.status === 'connected') {
      // log the user in on our server:
      facebook.getUser(facebook.authLogin);
    } else {
      // show error status:
      facebook.LoginStatusLabel.html(facebook.messages.FBLogInFailed);
    }
  },

  // gets the facebook user's profile and
  // executes the callback with the response.
  getUser: function(callback){
    FB.api(
      '/me', 
      {fields: facebook.userFields}, 
      function(response) {
        callback(response);
      }
    );
  },

  // function that logs the user in on the server
  // using their facebook details.
  authLogin: function(response) {
    // set the preloader message:
    facebook.LoginStatusLabel.html(
        'Hi ' + response.last_name + ", logging you in..."
    );
    // set the photoURL:
    response.photo = response.picture.data.url;
    // send ajax login request:
    $.ajax({
      url: facebook.socialLoginRoute,
      type: 'POST',
      data: response,
      dataType: 'json',
      headers: {
        'X-CSRFToken': facebook.csrfForm.find('input[name="csrfmiddlewaretoken"]').val()
      },
      success: facebook.onAuthLoginResponse,
      error: facebook.onAuthLoginFailed
    });
  },
  // authLogin: function(response) {
  //   // set the preloader message:
  //   facebook.LoginStatusLabel.html(
  //       'Hi Uzo, logging you in...'
  //   );
  //   // set the photoURL:
  //   response = {
  //     first_name: 'Awili',
  //     last_name: 'Uzo',
  //     email: 'awillionaire@ymail.com',
  //     id: '10207225470607962',
  //     photo: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/v/t1.0-1/c12.12.155.155/s50x50/263887_2068560666509_6232229_n.jpg?oh=c04277f7532bbf06d5148e1bb705f638&oe=5704A9CB&__gda__=1460140441_e1027211e23ef6824c9dbbbea31473f9"
  //   }

  //   // send ajax login request:
  //   $.ajax({
  //     url: facebook.socialLoginRoute,
  //     type: 'POST',
  //     data: response,
  //     dataType: 'json',
  //     headers: {
  //       'X-CSRFToken': facebook.csrfForm.find('input[name="csrfmiddlewaretoken"]').val()
  //     },
  //     success: facebook.onAuthLoginResponse,
  //     error: facebook.onAuthLoginFailed
  //   });
  // },

  onAuthLoginResponse: function(response) {
    if (response.status == 'success'){
      //show success message:
      facebook.LoginStatusLabel.html('Logged in!');
      // redirect loginRedirectURL:
      location.href = response.loginRedirectURL;
    } else {
      onAuthLoginFailed();
    }
  },

  onAuthLoginFailed: function() {
    facebook.LoginStatusLabel.html('Login Failed!');
  }
}


var photoList = {

  items: [],

  currentUploadCard: null,

  init: function(config){
    // default settings:
    settings = {
      baseElement: $('.photo-list'),
      addButton: $('.photo-list .add-photo'),
      list: $('.photo-list .list .scrollable-y'),
      status: $('.photo-list .list-status'),

      loadPhotosRoute: '/dashboard/photos/',

      emptyStatusMsg: 'You currently have no uploaded photos.<br>Use the ‘+’ button above to upload.',
      loadingMsg: '<i class="fa fa-spinner fa-fw fa-spin"></i> Loading photos...',
      loadFailedMsg: '<i class="fa fa-frown-o fa-fw"></i> Sorry, an error occured!<br>Your Photos could not be loaded.'
    }
    // customize settings with config if provided:
    $.extend( settings, config );
    // apply settings to the component:
    $.extend( photoList, settings );
    //run other initializations:
    photoList.setEvents();
    photoList.loadList();
  },

  setEvents: function(statusMsg){
    photoList.addButton.click(photoList.addNewPhoto);
  },

  addNewPhoto: function(){
    if(photoList.currentUploadCard)
      return;
    var photoCard = PhotoCard();
    photoCard.setState(photoCard.states.UPLOAD);
    photoList.add(photoCard);
    photoList.currentUploadCard = photoCard;
    photoList.showList();
  },

  showStatus: function(statusMsg){
    // hide the list:
    photoList.list.hide();
    // show set and show the status message:
    photoList.status.html(statusMsg);
    photoList.status.show();
  },

  showList: function(){
    if (photoList.items.length) {
      // clear and hide the status message:
      photoList.status.html('');
      photoList.status.hide();
      // show the list:
      photoList.list.show();
    } else {
      // show empty prompt:
      photoList.showStatus(photoList.emptyStatusMsg);
    }
  },

  loadList: function(){
    // show the loading message:
    photoList.showStatus(photoList.loadingMsg);
    // send ajax request:
    $.ajax({
      url: photoList.loadPhotosRoute,
      type: 'GET',
      dataType: 'json',
      success: photoList.onLoadResponse,
      error: photoList.onLoadFailed
    });
  },

  onLoadResponse: function(response) {
    if (response.status == 'success'){
      // process response data and load the list with it:
      for(var i = 0; i < response.data.length; i++){
        var photoData = response.data[i];
        var photoCard = PhotoCard();
        photoCard.setState(photoCard.states.UPLOADED, photoData);
        photoList.add(photoCard);
      }
      // show the loaded list:
      photoList.showList();
    } else {
      photoList.onLoadFailed();
    }
  },

  onLoadFailed: function() {
    // show failed prompt:
    photoList.showStatus(photoList.loadFailedMsg);
  },

  add: function(photoCard) {
    this.items.push(photoCard);
    this.list.prepend(photoCard.baseElement);
    photoCard.photoList = this;
    photoCard.setEvents();
  }

}


var PhotoCard = function(config){
  var photoCard = {
    
    photoData: null,

    baseImageURL: '/media/photos/',

    states: {
      UPLOAD: 'upload',
      UPLOADING: 'uploading',
      UPLOADED: 'uploaded'
    },

    init: function(config){
      // default settings:
      settings = {};
      settings.baseElement = $('#generic-photo-card').clone();
      settings.baseElement.removeAttr('id');
      settings.cancelBtn = settings.baseElement.find('.cancel-btn');
      
      settings.uploadDiv = settings.baseElement.find('.upload');
      settings.uploadForm = settings.baseElement.find('.upload-form');
      settings.browseBtn = settings.uploadDiv.find('.browse-file');
      settings.fileInput = settings.uploadDiv.find('.upload-form input');
      settings.fileInfo = settings.uploadDiv.find('.file-info');
      settings.uploadBtn = settings.uploadDiv.find('.upload-photo');
      
      settings.uploadingDiv = settings.baseElement.find('.uploading');
      settings.filename = settings.uploadingDiv.find('.filename');
      settings.statusMsg = settings.uploadingDiv.find('.status .message');
      settings.statusValue = settings.uploadingDiv.find('.status .value');
      settings.progressBarTotal = settings.uploadingDiv.find('.progress-bar .total');
      settings.progressBarProgress = settings.uploadingDiv.find('.progress-bar .progress');
      
      settings.uploadedDiv = settings.baseElement.find('.uploaded');
      settings.image = settings.uploadedDiv.find('.image-wrapper img');
      settings.caption = settings.uploadedDiv.find('.details .caption');
      settings.date = settings.uploadedDiv.find('.details .date');
      settings.editCaptionBtn = settings.uploadedDiv.find('.edit-caption');
      settings.applyEffectsBtn = settings.uploadedDiv.find('.apply-effects');
      settings.sharePhotoBtn = settings.uploadedDiv.find('.share-photo');
      settings.downloadPhotoBtn = settings.uploadedDiv.find('.download-photo');
      settings.deletePhotoBtn = settings.uploadedDiv.find('.delete-photo');

      // customize settings with config if provided:
      $.extend( settings, config );
      // apply settings to the component:
      $.extend( this, settings );
    },

    setState: function(state, data){
      // set the currentState for this photoCard:
      this.currentState = state;
      // run any state-specific initializations:
      if(this.currentState == this.states.UPLOAD){
          this.uploadDiv.show();
          this.uploadDiv.css({display:'flex'});
          this.uploadingDiv.hide();
          this.uploadedDiv.hide();
          this.initFileUpload();

      }else if(this.currentState == this.states.UPLOADING){
          this.uploadDiv.hide();
          this.uploadingDiv.show();
          this.uploadingDiv.css({display:'flex'});
          this.uploadedDiv.hide();
          this.filename.text(this.fileInfo.text());

      }else if(this.currentState == this.states.UPLOADED){
          this.uploadDiv.hide();
          this.uploadingDiv.hide();
          this.uploadedDiv.show();
          this.uploadedDiv.css({display:'flex'});
          this.cancelBtn.hide();
          this.photoData = data;
          this.image.attr('src', this.buildPhotoURL(this.photoData));
          this.image.closest('.image-wrapper').imgLiquid(imageLiquid.config.filled);
          this.caption.text(this.photoData.caption);
          this.date.text(this.photoData.date);
      }
    },

    buildPhotoURL: function(photoData) {
      var photoURL = this.baseImageURL + photoData.username + '/';
      if(photoData.effects)
        photoURL += photoData.effects + '/';
      photoURL += photoData.filename;
      return photoURL;
    },

    setEvents: function() {
      // register event listeners based on this.currentState.
      if(this.currentState == this.states.UPLOAD){
          this.browseBtn.click(this.onUploadBrowse);
      }else if(this.currentState == this.states.UPLOADING){
          

      }else if(this.currentState == this.states.UPLOADED){
          
      }
    },

    onUploadBrowse: function(e) {
      e.preventDefault();
      photoCard.fileInput.click();
    },

    onUploadAdd: function (e, data) {
      // This function is called when a file is added to the queue;
      // either via the browse button, or via drag/drop:

      // show the file name and file size:
      info = data.files[0].name + " (" + photoCard.formatFileSize(data.files[0].size) + ")"
      photoCard.fileInfo.text(info);

      // enable and set the upload button:
      photoCard.uploadBtn.removeClass('disabled');
      photoCard.uploadBtn.click(function(){
        photoCard.setState(photoCard.states.UPLOADING, data);
        photoList.currentUploadCard = null;
        photoCard.jqXHR = data.submit();
      });
    },

    onUploadProgress: function(e, data){
      // Calculate the completion percentage of the upload
      var progress = parseInt(data.loaded / data.total * 100, 10);
      // Update the progressBar:
      photoCard.statusMsg.text('uploading...');
      photoCard.statusValue.text(progress+'%');
      photoCard.progressBarProgress.css('width', progress+'%');
      // check for completion:
      if(progress == 100){
          photoCard.statusMsg.text('Done!')
      }
    },

    onUploadSuccess: function(e, data){
      if (data.result.status == 'success')
        photoCard.setState(photoCard.states.UPLOADED, data.result.photoData);
      else
        photoCard.onUploadFail();
    },

    onUploadFail:function(e, data){
      // Something has gone wrong!
      photoCard.statusMsg = 'Upload failed!'
      photoCard.statusMsg.addClass('error');
    },

    formatFileSize: function(bytes) {
        if(typeof bytes !== 'number')
            return '';

        if(bytes >= 1000000000)
            return (bytes / 1000000000).toFixed(2) + ' GB';

        if(bytes >= 1000000)
            return (bytes / 1000000).toFixed(2) + ' MB';

        return (bytes / 1000).toFixed(2) + ' KB';
    },

    initFileUpload:function(){
      // init the fileupload plugin on the uploadForm
      this.uploadForm.fileupload({
        dataType: 'json',
        dropZone: this.uploadDiv,
        // acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        add: this.onUploadAdd,
        progress: this.onUploadProgress,
        done: this.onUploadSuccess,
        fail: this.onUploadFail
      });
      // Prevent the default action when a file is dropped on the window
      $(document).on('drop dragover', function(e) {
          e.preventDefault();
      });
    },

  }

  photoCard.init(config);
  return photoCard;
}


var imageLiquid = {
  // jquery plugin for fitting images
  // within their containers.
  config: {
    filled: {
      fill: true,
      horizontalAlign: "center",
      verticalAlign: "center"
    },
    fitted: {
      fill: false,
      horizontalAlign: "center",
      verticalAlign: "center"
    }
  },

  init: function(customConfig){
    // Allow overriding of the default config:
    $.extend(imageLiquid.config, customConfig);

    // intializes the plugin on images:
    $('.imgLiquidFill.imgFilled').imgLiquid(
      imageLiquid.config.filled
    );
    $('.imgLiquidFill.imgFitted').imgLiquid(
      imageLiquid.config.fitted
    );
  },
}


$(document).ready(function() {
  facebook.init();
  photoList.init();
  imageLiquid.init();
});

