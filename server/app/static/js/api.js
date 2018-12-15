export function startActivity(expense) {
  return fetch("/api/expense/create", {
    method: 'POST',
    body: JSON.stringify( {
      ...expense,
      started_at: moment().toISOString().substr(0,19)
    } ), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(response => response.expense._id.$oid)
  .catch(error => console.error('Error:', error))
}

export function finishActivity(expenseId) {
  return fetch(`/api/expense/update/${expenseId}`, {
    method: 'POST',
    body: JSON.stringify( {
      finished_at: moment().toISOString().substr(0,19)
    } ), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(response => response.expense)
  .catch(error => console.error('Error:', error))
}

function getTimeLogGroups(startDate, endDate) {
  return fetch(`/api/expense/date_groups/${startDate}/${endDate}/`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => JSON.parse(response.expense_groups))
  .then(expenseGroups => expenseGroups.map(populateGroupedExpansesWithSkillsData))
  .catch(error => console.error('Error:', error))
}

export function getThisMonthDateLogGroups() {
  const today = moment();
  const startDate = today.startOf('month').toISOString().substring(0,10);
  const endDate = today.endOf('month').toISOString().substring(0,10);
  return getTimeLogGroups(startDate, endDate);
}


export function getSkillById(skillId) {
  const currentId =  typeof skillId === "object" ? skillId.skill : skillId
  return activeSkills.find(
    ({_id}) => _id.$oid == currentId
  )
}

function populateGroupedExpansesWithSkillsData(group) {
  const skill = getSkillById(group._id);
  if(skill) {
    group = {
      ...group,
      name: skill.name,
      target: skill.target_day,
      color: skill.color || "#000000" };
    group.achievedTarget = group.total * 100 / (group.target * 7); //day's target to week
  }
  return group;
}

function getActitivityGroups(startDate, endDate) {
  return fetch(`/api/expense/groups/${startDate}/${endDate}/`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => JSON.parse(response.expense_groups))
  .then(expenseGroups => expenseGroups.map(populateGroupedExpansesWithSkillsData))
  .catch(error => console.error('Error:', error))
}

export function getTodaysActivityGroups() {
  // today
  let startDate = new Date().toISOString().substr(0,10);
  // tomorrow
  let endDate = new Date(new Date().setDate((new Date().getDate() + 1))).toISOString().substring(0,10);
  return getActitivityGroups(startDate, endDate);
}

export function getThisWeekActivityGroups() {
  const today = moment();
  const startDate = today.startOf('week').toISOString().substring(0,10);
  const endDate = today.endOf('week').toISOString().substring(0,10);
  return getActitivityGroups(startDate, endDate);
}

export function getPreviousWeekActivityGroups() {
  const startDate = moment().subtract(1, 'weeks').startOf('week').toISOString().substring(0,10);
  const endDate = moment().subtract(1, 'weeks').endOf('week').toISOString().substring(0,10);
  return getActitivityGroups(startDate, endDate);
}
