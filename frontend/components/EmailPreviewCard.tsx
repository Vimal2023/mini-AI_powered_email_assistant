type EmailPreviewProps = {
  index: number;
  from: string;
  subject: string;
  summary: string;
};

export function EmailPreviewCard({
  index,
  from,
  subject,
  summary,
}: EmailPreviewProps) {
  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm hover:shadow-lg hover:-translate-y-[1px] transition cursor-pointer">
      <p className="text-[11px] text-gray-400 mb-1">Email #{index}</p>
      <p className="font-semibold text-sm text-blue-600">{subject}</p>
      <p className="text-gray-600 text-xs mt-1">From: {from}</p>
      <p className="text-gray-700 text-sm mt-2">{summary}</p>
    </div>
  );
}
