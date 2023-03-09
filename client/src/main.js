// external libraries
import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCalendarDays, faChevronDown, faChevronRight, faCircleExclamation, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

// local imports
import App from './App.vue'
import router from './router'

// global styles
import './styles/global.scss';
import 'v-calendar/dist/style.css';

library.add(faCalendarDays, faChevronDown, faChevronRight, faCircleExclamation, faGithub, faSpinner);

const app = createApp(App);

app.use(router);
app.component('FontAwesomeIcon', FontAwesomeIcon);
app.mount('#app');