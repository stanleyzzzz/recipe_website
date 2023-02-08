/* HELPER FILE FOR FUNCTIONS */

// Posts data to url using fetch
// Returns a promsise
export function postData(url, data, token = '') {
    return fetch(url, {
      method: 'post',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data),
    }).then((response) => {
      // checking if there is an error
      return response.json();
    });
  }

  // Fetches data (GET)
  // Takes in a url that's the path we're getting from
  // Takes in a token to make sure the user is signed in
  // Shows an error modal to the user on failure
  export function getData(url, token) {
    return fetch(url, {
      method: 'get',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  }

  // Fetches data (PUT)
  // Takes in a url that's the path we're updating
  // Takes in data, the information that is being changed
  // Takes in a token to make sure the user is signed in
  // Shows an error modal to the user on failure
  export function updateData(url, data, token) {
    return fetch(url, {
      method: 'put',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data),
    }).then((response) => {
      return response.json();
    });
  }

  // Deletes data (DELETE)
  // Takes in a url to whatever information we're deleting
  // Takes in a token to make sure the user is signed in
  // Shows an error modal to the user on failure
  export function deleteData(url, data, token) {
    return fetch(url, {
      method: 'delete',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data)
    }).then((response) => {
      // checking if there is an error
      return response.json();
    });
  }
