
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
    // FB.login(
    //   facebook.onFBLoginResponse,
    //   {scope: 'email,user_likes'}
    // );
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
  // authLogin: function(response) {
  //   // set the preloader message:
  //   facebook.LoginStatusLabel.html(
  //       'Hi ' + response.last_name + ", logging you in..."
  //   );
  //   // set the photoURL:
  //   response.photo = response.picture.data.url;
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
  authLogin: function(response) {
    // set the preloader message:
    facebook.LoginStatusLabel.html(
        'Hi Uzo, logging you in...'
    );
    // set the photoURL:
    response = {
      first_name: 'Awili',
      last_name: 'Uzo',
      email: 'awillionaire@ymail.com',
      id: '10207225470607962',
      photo: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/v/t1.0-1/c12.12.155.155/s50x50/263887_2068560666509_6232229_n.jpg?oh=c04277f7532bbf06d5148e1bb705f638&oe=5704A9CB&__gda__=1460140441_e1027211e23ef6824c9dbbbea31473f9"
    }

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

imageLiquid = {
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


var photoList = {

  items: [],

  init: function(config){
    // default settings:
    settings = {
      baseElement: $('.photo-list'),
      addButton: $('.photo-list .add-photo'),
      list: $('.photo-list .list'),
      status: $('.photo-list .list-status'),

      loadPhotosRoute: '/dashboard/photos/',

      emptyStatusMsg: 'You currently have no uploaded photos.<br>Use the ‘+’ button above to upload.',
      loadingMsg: '<i class="fa fa-spinner fa-fw fa-spin"></i> Loading...',
      loadFailedMsg: '<i class="fa fa-frown-o fa-fw"></i> Sorry, an error occured. Your Photos could not be loaded!'
    }
    // customize settings with config if provided:
    $.extend( settings, config );
    // apply settings to the component:
    $.extend( photoList, settings );
    //run other initializations:
    photoList.registerEventHandlers();
    photoList.loadList();
  },

  registerEventHandlers: function(statusMsg){
    photoList.addButton.click(photoList.onAddPhotoClicked);
  },

  onAddPhotoClicked: function(){
    console.log('+ add-photo button clicked!');
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
      for(photo_data in response.data){
        
      }
      // show the loaded list:
      photoList.showList();
    } else {
      onLoadFailed();
    }
  },

  onLoadFailed: function() {
    // show failed prompt:
    photoList.showStatus(photoList.loadFailedMsg);
  }

}


$(document).ready(function() {
  facebook.init();
  imageLiquid.init();
  photoList.init();
});

