import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import axios from "axios";

interface ResumeState {
  resume: string;
  jobDescription: string;
  resumeSkills: string[];
  jobSkills: string[];
  suggestedSkills: string[];
  selectedSkills: string[];
  regeneratedResume: string;
  loading: boolean;
  error: string | null;
}

const initialState: ResumeState = {
  resume: "",
  jobDescription: "",
  resumeSkills: [],
  jobSkills: [],
  suggestedSkills: [],
  selectedSkills: [],
  regeneratedResume: "",
  loading: false,
  error: null,
};

export const analyzeResume = createAsyncThunk(
    "resume/analyzeResume",
    async (
        {
          resume_text,
          job_description_text,
        }: { resume_text: string; job_description_text: string },
        { rejectWithValue }
    ) => {
      try {
        const response = await axios.post("http://localhost:5000/extract_skills", {
          resume_text,
          job_description_text,
        });
        return response.data;
      } catch (error: any) {
        return rejectWithValue(error.response?.data || "Error analyzing resume");
      }
    }
);

const resumeSlice = createSlice({
  name: "resume",
  initialState,
  reducers: {
    setResume(state, action: PayloadAction<string>) {
      state.resume = action.payload;
    },
    setJobDescription(state, action: PayloadAction<string>) {
      state.jobDescription = action.payload;
    },
    setSelectedSkills(state, action: PayloadAction<string[]>) {
      state.selectedSkills = action.payload;
    },
    setRegeneratedResume(state, action: PayloadAction<string>) {
      state.regeneratedResume = action.payload;
    },
    applyRegeneratedResume(state) {
      if (state.regeneratedResume) {
        state.resume = state.regeneratedResume;
        state.regeneratedResume = "";
      }
    },
  },
  extraReducers: (builder) => {
    builder
        .addCase(analyzeResume.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(analyzeResume.fulfilled, (state, action) => {
          state.loading = false;
          state.resumeSkills = action.payload.resume_skills;
          state.jobSkills = action.payload.job_skills;
          state.suggestedSkills = action.payload.suggested_skills;
        })
        .addCase(analyzeResume.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload as string;
        });
  },
});

export const {
  setResume,
  setJobDescription,
  setSelectedSkills,
  setRegeneratedResume,
  applyRegeneratedResume,
} = resumeSlice.actions;

export default resumeSlice.reducer;