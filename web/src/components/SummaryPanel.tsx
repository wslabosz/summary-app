type SummaryPanelProps = {
  summary: string;
  videoTitle: string;
};

export const SummaryPanel = ({
  summary,
  videoTitle,
}: SummaryPanelProps) => {
  return (
    <div>
      <h1>Summary Panel</h1>
      <p>Video Title: {videoTitle}</p>
      <p>Summary: {summary}</p>
    </div>
  );
};
