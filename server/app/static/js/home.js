import { startActivity, finishActivity } from "./api.js?version=2"
import { showNotification } from "./notifications.js?version=1"
const TIMER_STEP = 30

if(document.querySelector("#home")) {
new Vue({
  el: '#home',
  data: {
    selectedAmountOfTime: 15,
    isActivityStarted: false,
    timerProgress: 0,
    timePassedSec: 0,
    activityTimer: null,
    expense: {
      skill: '',
      amount: 15
    }
  },
  methods: {
    onActivityStart,
    onActivityStop,
  },
  computed: {
    timeProgressBarText: function () {
      if(!this.isActivityStarted) return "";
      return `${this.timerProgress}/${this.expense.amount * 60} seconds`;
    },
    timerProgressInPercents: function () {
      if(!this.isActivityStarted) return 0;
      const percentsOfTimePerSecond = 100/(+this.expense.amount * 60);
      return this.timerProgress*percentsOfTimePerSecond;
    }
  }
})

function clearProgress() {
  this.isActivityStarted = false;
  this.timerProgress = 0;
  clearInterval(this.activityTimer);
}

function getSkillNameById(skillId) {
  return activeSkills.find(
    ({_id}) => _id.$oid == this.expense.skill
  ).name || ""
}

function onActivityStart() {
  startActivity(this.expense);
  this.isActivityStarted = true;
  this.activityTimer = setInterval(() => {
    this.timerProgress += TIMER_STEP;
    if(this.timerProgress >= this.expense.amount * 60) {
      finishActivity(this.expense);
      const selectedActivityName = getSkillNameById(this.expense.skill);
      showNotification("Good job!",
        `${this.expense.amount} minutes sucessfully invested into ${selectedActivityName}`);
      clearProgress.apply(this);
    }
  }, 1000)
}

function onActivityStop() {
  if(window.confirm("If you stop activity progress will be lost. (Sorry, there isn't pause - you can't pause the time.)")) {
    clearProgress.apply(this);
  }
}
// Day time countdown
(function() {
  const timeLeftElement = document.querySelector("#expenses-list-time-left")
  const currentUnixTime = new Date().getTime() / 1000;
  const endOfTheCurrentDay = (new Date()).setHours(23,59,59,999)
  const endOfTheCurrentDayUnixTime = endOfTheCurrentDay / 1000

  let minutesLeftInTheCurrentDay = (endOfTheCurrentDayUnixTime - currentUnixTime) / 60
  minutesLeftInTheCurrentDay =  Math.round(minutesLeftInTheCurrentDay)
  timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
  setInterval(() => {
    if(minutesLeftInTheCurrentDay > 0)
      minutesLeftInTheCurrentDay--
    else location.reload();
    timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
  }, 1000*60);
})()
}
