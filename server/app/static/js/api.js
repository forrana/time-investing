export function startActivity(expense) {
  return fetch("/api/expense/create", {
    method: 'POST',
    body: JSON.stringify( {
      ...expense,
      started_at: new Date().toISOString().substr(0,19)
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
      finished_at: new Date().toISOString().substr(0,19)
    } ), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(response => response.expense)
  .catch(error => console.error('Error:', error))
}

export function getTodaysActivityGroups(
    // today
    start_date = new Date().toISOString().substr(0,10),
    // tomorrow
    end_date = new Date(new Date().setDate((new Date().getDate() + 1))).toISOString().substring(0,10)
  ) {
  return fetch(`/api/expense/groups/${start_date}/${end_date}`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => response)
  .catch(error => console.error('Error:', error))
}
