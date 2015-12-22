
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
    console.log(response);
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
    backgrounds: {
      fill: true,
      horizontalAlign: "center",
      verticalAlign: "center"
    },
    thumbnails: {
      fill: true,
      horizontalAlign: "center",
      verticalAlign: "center"
    },
    editor: {
      fill: false,
      horizontalAlign: "center",
      verticalAlign: "center"
    }
  },

  init: function(customConfig){
    // Allow overriding of the default config:
    $.extend(imageLiquid.config, customConfig);

    // intializes the plugin on images:
    $('.imgLiquidFill.bg-image').imgLiquid(
      imageLiquid.config.backgrounds
    );
    $('.imgLiquidFill.thumb-image').imgLiquid(
      imageLiquid.config.thumbnails
    );
    $('.imgLiquidFill.editor-image').imgLiquid(
      imageLiquid.config.editor
    );
  },
}


$(document).ready(function() {
  facebook.init();
  imageLiquid.init();
});

