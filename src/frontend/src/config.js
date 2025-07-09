const config = {
  api: {
    baseUrl: process.env.NODE_ENV === 'production'
      ? 'https://media-assistant-api.azurewebsites.net'
      : 'http://localhost:7071',
    endpoints: {
      query: '/api/query',
      preferences: '/api/user/preferences'
    }
  },
  speech: {
    subscriptionKey: process.env.REACT_APP_SPEECH_KEY,
    region: 'eastus'
  }
};

export default config;
