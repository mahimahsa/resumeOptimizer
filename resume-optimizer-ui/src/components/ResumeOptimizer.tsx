'use client';
import { useDispatch, useSelector } from "react-redux";
import { setResume, setJobDescription, analyzeResume } from "../store/resumeSlice";
import { AppDispatch } from "../store";
import SuggestedSkillsSelector from "./SuggestedSkillsSelector";


const ResumeOptimizer = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { resume, jobDescription, resumeSkills, jobSkills,suggestedSkills, loading, error } = useSelector(
    (state: any) => state.resume
  );

  const handleOptimizeResume = () => {
    dispatch(
      analyzeResume({
        resume_text: resume,
        job_description_text: jobDescription,
      })
    );
  };

  return (
    <div className="flex flex-col items-center p-6 max-w-2xl mx-auto">
    <h1 className="text-2xl font-bold text-center mb-8 ">AI-Powered Resume Optimizer</h1>
    <p className="text-gray-600 text-sm font-bold text-center mb-6">
      Paste your resume and job description to find missing keywords and improve alignment.
    </p>
    <div className="w-full flex flex-col gap-4">
      <textarea
        className="border p-3 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows={6}
        placeholder="Paste your Resume here..."
        value={resume}
        onChange={(e) => dispatch(setResume(e.target.value))}
      />

      <textarea
        className="border p-3 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows={6}
        placeholder="Paste the Job Description here..."
        value={jobDescription}
        onChange={(e) => dispatch(setJobDescription(e.target.value))}
      />
      </div>
      <button
        className="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700"
        onClick={handleOptimizeResume}
        disabled={loading}
      >
        {loading ? "Optimizing..." : "Optimize Resume"}
      </button>

      {error && <p className="text-red-500">{error}</p>}

      <div className="mt-6 w-full p-4 bg-gray-100 rounded-lg">
          <h2 className="text-lg font-semibold">Job Skills:</h2>
        <ul>
          {jobSkills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
      </div>
      <div className="mt-6 w-full p-4 bg-gray-100 rounded-lg">
      <h2 className="text-lg font-semibold">Resume Skills:</h2>
        <ul>
          {resumeSkills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
      </div>
      {/*{suggestedSkills.length > 0 && (*/}
          <SuggestedSkillsSelector suggestedSkills={suggestedSkills} />
      {/*)}*/}

    </div>
  );
};

export default ResumeOptimizer;