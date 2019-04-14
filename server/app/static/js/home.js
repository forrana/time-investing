import {
  startActivity,
  finishActivity,
  getTodaysActivityGroups,
  getThisWeekActivityGroups,
  getPreviousWeekActivityGroups,
  getThisMonthDateLogGroups,
  getSkillById
} from "./api.js?version=46"
import { showNotification } from "./notifications.js?version=1"
const TIMER_STEP = 60


if(document.querySelector("#home")) {
  // Data revieved from server through global vars
  (async function() {
    const defaultTime = defaultTimeFlask || 0;

    const groupedExpansesWSkillData = await getTodaysActivityGroups();
    const groupedExpansesCurrentWeekWSkillData = await getThisWeekActivityGroups();
    const groupedExpansesPreviousWeekWSkillData = await getPreviousWeekActivityGroups();
    const groupedByDateThisMonthExpenses = await getThisMonthDateLogGroups();

    Vue.component('progress-bar', {
      props: ['color', 'percents', 'minutesTotal', 'minutesTarget'],
      template:`
        <div class="progress">
          <div
            class="progress-bar"
            role="progressbar"
            v-bind:style="{width: percents + '%', backgroundColor: color}"
            v-bind:aria-valuenow="percents"
            aria-valuemin="0"
            aria-valuemax="100">
          </div>
          <span class="progress-bar-title">
            {{minutesTotal}}/{{minutesTarget}} minutes
          </span>
        </div>
      `
    })

    Vue.component('progressbar-combined', {
      props: ['expenses', 'localTotal'],
      methods: {
        groupeAchievedInProportion: function(group, total) {
          return group.total * 100 / total;
        },
      },
      template:`
      <div class="progress">
          <div
            v-for="expense in expenses"
            class="progress-bar"
            role="progressbar"
            v-bind:style="{width: groupeAchievedInProportion(expense, localTotal) + '%', backgroundColor: expense.color}"
            v-bind:aria-valuenow="groupeAchievedInProportion(expense, localTotal)"
            aria-valuemin="0"
            aria-valuemax="100">
          </div>
          <span class="progress-bar-title">
            {{localTotal}} minutes
          </span>
      </div>
      `
    })

    new Vue({
      el: '#home',
      data: {
        isActivityStarted: false,
        timerProgress: 0,
        timePassedSec: 0,
        activityTimer: null,
        currentDayNumber: moment().date(),
        currentMonthNumber: moment().month(),
        currentYearNumber: moment().year(),
        expense: {
          skill: '',
          amount: defaultTime
        },
        expenseGroups: groupedExpansesWSkillData,
        expenseThisWeekGroups: groupedExpansesCurrentWeekWSkillData,
        expensePreviousWeekGroups: groupedExpansesPreviousWeekWSkillData,
        expenseThisMonthGroups: groupedByDateThisMonthExpenses,
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
        groupeAchievedInProportion: function(group, total) {
          return group.total * 100 / total;
        },
        getTodaysExpenses: function(dayNumber) {
          return this.expenseThisMonthGroups
            .filter(({_id}) => _id.day == dayNumber)
            .sort((expenseA, expenseB) => {
                if(expenseA.color < expenseB.color) return -1;
                if(expenseA.color > expenseB.color) return 1;
                return 0;
              })
        },
        getTodaysTotal: function(dayNumber) {
          return this.expenseThisMonthGroups
            .filter(({_id}) => _id.day == dayNumber)
            .reduce((accumulator, expense) => accumulator + expense.total, 0)
        },
        getThisMonthTotal: function(dayNumber) {
          return this.expenseThisMonthGroups
            .reduce((accumulator, expense) => accumulator + expense.total, 0)
        },
        getTodaysTotalPercentage: function(dayNumber) {
          return (1 + this.getTodaysTotal(dayNumber) / this.getThisMonthTotal(dayNumber))*100
        },
        getTodaysExpensePercentage: function(dayNumber, expense) {
          return (expense.total / this.getTodaysTotal(dayNumber)) * 100
        },
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
      const onActivityEnd = async () => {
        await finishActivity(this.expense.id);
        const selectedActivityName = getSkillById(this.expense.skill).name;
        clearProgress.apply(this);
        showNotification("Good job!",
          `${this.expense.amount} minutes sucessfully invested into ${selectedActivityName}`);
        this.expenseGroups = await getTodaysActivityGroups();
        this.expenseThisWeekGroups = await getThisWeekActivityGroups();
        this.expenseThisMonthGroups = await getThisMonthDateLogGroups();
      }

      const result = await startActivity(this.expense);
      this.expense.id= result;
      this.isActivityStarted = true;
      this.activityTimer = setInterval(async () => {
        this.timerProgress += TIMER_STEP;
        if(this.timerProgress >= this.expense.amount * 60) {
          onActivityEnd();
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
  const howManyMinutesLeftToday = () => {
    const currentUnixTime = new Date().getTime() / 1000;
    const endOfTheCurrentDay = (new Date()).setHours(23,59,59,999)
    const endOfTheCurrentDayUnixTime = endOfTheCurrentDay / 1000

    const minutesLeftInTheCurrentDay = (endOfTheCurrentDayUnixTime - currentUnixTime) / 60
    return Math.round(minutesLeftInTheCurrentDay)
  }

  const renderHowManyMinutesLeftToday = () => {
    const timeLeftElement = document.querySelector("#expenses-list-time-left")
    const minutesLeftInTheCurrentDay = howManyMinutesLeftToday();
    if(minutesLeftInTheCurrentDay > 0)
      timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
    else location.reload();
  }

  renderHowManyMinutesLeftToday();
  setInterval(renderHowManyMinutesLeftToday, 1000*60);
  document.addEventListener( 'visibilitychange' , () => {
    if (!document.hidden) {
      renderHowManyMinutesLeftToday();
    }
  }, false );

})()
}
