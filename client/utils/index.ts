import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
dayjs.extend(utc);

export const toDate = (dateString: string, includeTime = true) => {
  return dayjs
    .utc(dateString)
    .local()
    .format(`MMM D YYYY ${includeTime ? "h:mma" : ""}`);
};
