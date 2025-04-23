"use client";
import { useSelector } from "react-redux";
import { RootState } from "../store";

const RegeneratedResume = () => {
  const regenerated = useSelector((state: RootState) => state.resume.regeneratedResume);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(regenerated);
    alert("Resume copied to clipboard!");
  };

  if (!regenerated) return null;

  return (
    <div className="mt-6 w-full p-4 bg-gray-100 rounded-lg">
      <h2 className="text-lg font-semibold mb-2">Regenerated Resume</h2>
      <pre className="bg-white p-4 text-sm whitespace-pre-wrap border rounded">{regenerated}</pre>
      <button
        onClick={handleCopy}
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Copy
      </button>
    </div>
  );
};

export default RegeneratedResume;
