import axios from "axios";

// TODO: convert the links to be based on prod environment or development, or implement a proxy
export const getUserFollowedRepositories = async () => {
  const response = await axios({
    method: "GET",
    url: "http://localhost:5000/flask/followed",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });

  return response;
};

export const getUserImportRepositories = async () => {
  const response = await axios.get("http://localhost:5000/flask/import");
  return response;
};

export const postUserLogin = async (values) => {
  const response = await axios.post("http://localhost:5000/flask/auth", {
    code: values,
  });

  return response;
};

export const getUserLogin = async () => {
  const response = await axios({
    method: "GET",
    url: "http://localhost:5000/flask/auth",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });

  return response;
};

export const postSearchGithub = async (value) => {
  const response = await axios({
    method: "POST",
    url: "http://localhost:5000/flask/search",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const postFollowRepository = async (value) => {
  const response = await axios({
    method: "POST",
    url: "http://localhost:5000/flask/follow",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const deleteUserRepository = async (value) => {
  const response = await axios({
    method: "DELETE",
    url: "http://localhost:5000/flask/followed",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const getForkClustering = async (value) => {
  const response = await axios({
    method: "GET",
    url: `http://localhost:5000/flask/cluster?repo=${value}`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });

  return response;
};
