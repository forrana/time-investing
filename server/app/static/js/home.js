import { startActivity, finishActivity, getTodaysActivityGroups, getThisWeekActivityGroups, getPreviousWeekActivityGroups } from "./api.js?version=28"
import { showNotification } from "./notifications.js?version=1"
const TIMER_STEP = 60


if(document.querySelector("#home")) {
  // Data revieved from server through global vars
  (async function() {
    const defaultTime = defaultTimeFlask || 0;

    const groupedExpansesWSkillData = await getTodaysActivityGroups();
    const groupedExpansesCurrentWeekWSkillData = await getThisWeekActivityGroups();
    const groupedExpansesPreviousWeekWSkillData = await getPreviousWeekActivityGroups();

    new Vue({
      el: '#home',
      data: {
        isActivityStarted: false,
        timerProgress: 0,
        timePassedSec: 0,
        activityTimer: null,
        expense: {
          skill: '',
          amount: defaultTime
        },
        expenseGroups: groupedExpansesWSkillData,
        expenseThisWeekGroups: groupedExpansesCurrentWeekWSkillData,
        expensePreviousWeekGroups: groupedExpansesPreviousWeekWSkillData
      },
      methods: {
        onActivityStart,
        onActivityStop,
        groupAchievedInPercentsWeek: function(group) {
          return group.total * 100 / (group.target*7);
        },
        groupAchievedInPercentsDay: function(group) {
          return group.total * 100 / group.target;
        },
        groupeAchievedInProportionDay: function(group, total) {
          return group.total * 100 / total;
        }
      },
      computed: {
        totalyInvestedToday: function () {
          return this.expenseGroups.reduce( (accumulator, {total}) => accumulator += total || 0, 0);
        },
        totalyInvestedThisWeek: function () {
          return this.expenseThisWeekGroups.reduce( (accumulator, {total}) => accumulator += total || 0, 0);
        },
        totalyInvestedPrviousWeek: function () {
          return this.expensePreviousWeekGroups.reduce( (accumulator, {total}) => accumulator += total || 0, 0);
        },
        timeProgressBarText: function () {
          if(!this.isActivityStarted) return "";
          return `${this.timerProgress}/${this.expense.amount * 60} seconds`;
        },
        timerProgressInPercents: function () {
          if(!this.isActivityStarted) return 0;
          const percentsOfTimePerSecond = 100/(+this.expense.amount * 60);
          return this.timerProgress*percentsOfTimePerSecond;
        },
      }
    })

    function clearProgress() {
      this.isActivityStarted = false;
      this.timerProgress = 0;
      clearInterval(this.activityTimer);
    }

    async function onActivityStart() {
      const result = await startActivity(this.expense);
      this.expense.id= result;
      this.isActivityStarted = true;
      this.activityTimer = setInterval(async () => {
        this.timerProgress += TIMER_STEP;
        if(this.timerProgress >= this.expense.amount * 60) {
          await finishActivity(this.expense.id);
          const selectedActivityName = getSkillById(this.expense.skill).name;
          clearProgress.apply(this);
          showNotification("Good job!",
            `${this.expense.amount} minutes sucessfully invested into ${selectedActivityName}`);
          this.expenseGroups = await getTodaysActivityGroups();
          this.expenseThisWeekGroups = await getThisWeekActivityGroups();
        }
      }, 1000)
    }

    function onActivityStop() {
      if(window.confirm("If you stop activity progress will be lost. (Sorry, there isn't pause - you can't pause the time.)")) {
        clearProgress.apply(this);
      }
    }
  })();
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
