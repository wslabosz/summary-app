import {
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import { useState } from "react";
import { useParams } from "react-router";
import { triggerSummary } from "../api/webhook";

type SummaryFormProps = {
  models: string[] | undefined;
  model: string | undefined;
  handleSetModel: (event: SelectChangeEvent) => void;
};

export const SummaryForm = ({
  models,
  model,
  handleSetModel,
}: SummaryFormProps) => {
  const params = useParams();
  const [forceSummary, setForceSummary] = useState(false);
  const handleCheckForceSummary = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setForceSummary(event.target.checked);
  };
  const onSubmit = async ({
    model,
    forceSummary,
  }: {
    model: string;
    forceSummary: boolean;
  }) => {
    const response = await triggerSummary({
      videoId: params.id as string,
      model,
      forceSummary,
    });
    console.log(response);
  };
  return (
    <FormControl className="nonDraggable" size="small">
      <InputLabel id="select-model-label">Model</InputLabel>
      <Select
        labelId="select-model-label"
        id="select-model"
        label="model"
        value={model}
        onChange={handleSetModel}
      >
        {models?.map((model) => (
          <MenuItem key={model} value={model}>
            {model}
          </MenuItem>
        ))}
      </Select>
      <FormControlLabel
        control={
          <Checkbox
            checked={forceSummary}
            onChange={handleCheckForceSummary}
            inputProps={{ "aria-label": "controlled" }}
          />
        }
        label="Force"
      />
      <Button
        onClick={() => onSubmit({ model: model as string, forceSummary })}
      >
        Summarize
      </Button>
    </FormControl>
  );
};
