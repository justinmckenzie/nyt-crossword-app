import { HTTP_STATUS } from "./constants";

export default async function fetcher(url) {
  try {
    const req = await fetch(url);
    const res = await req.json();

    if (res.status === HTTP_STATUS.SUCCESS) {
      return res;
    } else {
      throw new Error(res.message).toString();
    }
  } catch (err) {
    console.error(err);
    return { status: HTTP_STATUS.FAILURE, message: err, data: {} };
  }
}
