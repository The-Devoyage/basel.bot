"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { useWindowSize } from "@/shared/useWindowSize";
import HeatMap from "@uiw/react-heat-map";
import dayjs, { Dayjs } from "dayjs";
import { useThemeMode } from "flowbite-react";
import { Tooltip } from "react-tooltip";
import { useEffect, useState } from "react";

export const StandupHeatmap = () => {
  const themeMode = useThemeMode();
  const { windowSize } = useWindowSize();
  const [startDate, setStartDate] = useState<Dayjs>(
    dayjs().subtract(1, "year"),
  );
  const standups = useCallApi(
    {
      endpoint: Endpoint.GetStandups,
      query: {
        limit: 0,
        start_date: startDate.toDate(),
        end_date: dayjs().toDate(),
      },
      path: null,
      body: null,
    },
    { callOnMount: true },
  );

  useEffect(() => {
    if (!windowSize.width) return;

    if (windowSize.width >= 1280) {
      setStartDate(dayjs().subtract(10, "months"));
    } else if (windowSize.width >= 1200) {
      setStartDate(dayjs().subtract(8, "months"));
    } else if (windowSize.width >= 992) {
      setStartDate(dayjs().subtract(8, "months"));
    } else if (windowSize.width >= 768) {
      setStartDate(dayjs().subtract(5, "months"));
    } else if (windowSize.width >= 580) {
      setStartDate(dayjs().subtract(4, "months"));
    } else if (windowSize.width >= 487) {
      setStartDate(dayjs().subtract(3, "months"));
    } else {
      setStartDate(dayjs().subtract(85, "days"));
    }
  }, [windowSize]);

  const value = standups.res?.data?.reduce(
    (acc: { date: string; count: number }[], curr) => {
      const exists = acc.findIndex(
        (v) => v.date === curr.created_at.toString(),
      );
      if (exists >= 0) {
        acc[exists] = { ...acc[exists], count: acc[exists].count + 1 };
      } else {
        acc.push({ date: curr.created_at.toString(), count: 1 });
      }
      return acc;
    },
    [],
  );

  return (
    <>
      <HeatMap
        value={value}
        width="100%"
        height="100%"
        weekLabels={false}
        style={{
          color: themeMode.mode === "dark" ? "#FCE96A" : undefined,
        }}
        legendCellSize={0}
        rectSize={24}
        startDate={startDate.toDate()}
        rectRender={(props, data) => {
          const isFuture = dayjs(data.date).isAfter(dayjs());
          return (
            <rect
              {...props}
              fill={isFuture ? "#FBD5D5" : props.fill}
              opacity={isFuture ? 0.5 : props.opacity}
              data-tooltip-id="standup"
              data-tooltip-content={`${data.date}: ${data.count || 0} standups`}
            />
          );
        }}
        panelColors={{
          0: "#FDF6B2",
          7: "#FCE96A",
          14: "#FACA15",
          21: "#E3A008",
          28: "#C27803",
          35: "#9F580A",
        }}
      />
      <Tooltip id="standup" />
    </>
  );
};
