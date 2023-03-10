export default async function fetcher(url) {
  try {
    const req = fetch(url);
    const res = await (await req).json();

    if (res.status === 'success') {
      // TODO: change to just "res" when changes made to backend
      return { ...res, data: res.leaderboard };
    } else {
      console.log('in the else', res);
      throw new Error(res.message).toString();
    }
  } catch(err) {
    console.error(err);
    return { status: 'failure', message: err, data: {}};
  }
}
