import Vue from 'vue'
import VueMoment from 'vue-moment'

Vue.filter('capitalize', (value) => {
  if (!value) return ''
  let newVal = value
  newVal = newVal.toString()
  return newVal.charAt(0).toUpperCase() + newVal.slice(1)
})

Vue.use(VueMoment)
Vue.filter('humanizeTime', function (value) {
  let newVal = ''
  if (typeof value === 'string') {
    newVal = value.split('+')[0]
  } else if (typeof value === 'number') {
    newVal = value
  } else {
    return 'Not available'
  }
  return Vue.moment.utc(newVal).local().fromNow()
})

Vue.filter('calendarTime', function (value) {
  let newVal = ''
  if (typeof value === 'string') {
    newVal = value.split('+')[0]
  } else if (typeof value === 'number') {
    newVal = value
  } else {
    return 'Not available'
  }
  return Vue.moment.utc(newVal).local().calendar()
})
