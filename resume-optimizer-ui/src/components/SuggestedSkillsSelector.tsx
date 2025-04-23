"use client";

import { useDispatch, useSelector } from "react-redux";
import { setSelectedSkills, setRegeneratedResume } from "../store/resumeSlice";
import { AppDispatch } from "../store";
import { useState } from "react";



interface SuggestedSkillsSelectorProps {
    suggestedSkills: string[];
}

const SuggestedSkillsSelector = ({ suggestedSkills }: SuggestedSkillsSelectorProps) => {
    const dispatch = useDispatch<AppDispatch>();
    const resumeSkills = useSelector((state: any) => state.resume.resumeSkills);
    const [selected, setSelected] = useState<string[]>([]);
    const resume = useSelector((state: any) => state.resume.resume);
    const toggleSkill = (skill: string) => {
        setSelected((prev) =>
            prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
        );
    };

    const handleSubmit = async () => {
        dispatch(setSelectedSkills(selected));
        const response = await fetch("http://localhost:5000/finalize_skills", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_skills: resumeSkills,
            selected_skills: selected,
            resume_text: resume,
          }),
        });
      
        const result = await response.json();
        dispatch(setRegeneratedResume(result.regenerated_resume));
      };

    return (
        <div className="flex flex-col w-full mt-6 p-4 bg-gray-100 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Suggested Skills</h2>
            <div className="flex flex-wrap gap-2 mb-4">
                {suggestedSkills.map((skill) => (
                    <button
                        key={skill}
                        onClick={() => toggleSkill(skill)}
                        className={`px-4 py-2 rounded-full border text-sm font-medium transition ${
                            selected.includes(skill)
                                ? "bg-blue-600 text-white border-blue-600"
                                : "bg-white text-gray-700 border-gray-300 hover:bg-gray-100"
                        }`}
                    >
                        {skill}
                    </button>
                ))}
            </div>
            <button
                onClick={handleSubmit}
                className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
                Submit Selected Skills
            </button>
        </div>
    );
};

export default SuggestedSkillsSelector;