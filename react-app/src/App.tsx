// import CameraFeed from "./components/CameraView";

import { Loader2, Settings } from "lucide-react";
import { Switch } from "./components/ui/switch";
import { Label } from "./components/ui/label";
import { useEffect, useState } from "react";
import { Slider } from "./components/ui/slider";
import { cn } from "./lib/utils";

import { io } from "socket.io-client";
import { Progress } from "./components/ui/progress";

const socket = io("http://localhost:5000");

function App() {
  const [imgLoaded, setImgLoaded] = useState<boolean>(false);

  const [diseaseFilter, setDiseaseFilter] = useState<boolean>(false);
  const [detections, setDetections] = useState<boolean>(true);

  const [sensorVal, setSensorVal] = useState<number>(0);

  useEffect(() => {
    console.log("doing stuff");

    socket.on("connection", (_socket) => {
      console.log("connected");
    });

    socket.on("sensor", (data) => {
      console.log(data);
      setSensorVal(data.data);
    });
  }, []);

  async function toggleFilter(value: boolean) {
    // fetch the toggle_disease endpoint
    // the endpoint returns the current state of the filter as a string.

    setDiseaseFilter(value);

    const res = await fetch("http://localhost:5000/toggle_disease", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ toggle: value }),
    });

    const data = await res.json();
    console.log(data);
  }

  async function toggleDetections(value: boolean) {
    // fetch the toggle_disease endpoint
    // the endpoint returns the current state of the filter as a string.

    setDetections(value);

    const res = await fetch("http://localhost:5000/toggle_detections", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ toggle: value }),
    });

    const data = await res.json();
    console.log(data);
  }

  async function setThreshold(value: number) {
    // fetch the set_threshold endpoint
    // the endpoint returns the current state of the filter as a string.

    const res = await fetch("http://localhost:5000/set_threshold", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ threshold: value }),
    });

    const data = await res.json();
    console.log(data);
  }

  return (
    <main className="flex flex-col items-center justify-center h-screen">
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <div className="text-2xl text-left">Camera Feed</div>

          <Settings className="w-6 h-6" />
        </div>
        <img
          src="http://localhost:5000/video_feed"
          alt="random"
          className="w-[840px] h-[475px] rounded-md border mb-2"
          onLoad={() => setImgLoaded(true)}
          style={{
            display: imgLoaded ? "block" : "none",
          }}
        />
        {!imgLoaded && (
          <div className="w-[840px] h-[475px] rounded-md border mb-2 bg-muted flex items-center justify-center">
            <Loader2 className="w-24 h-24 animate-spin text-muted-foreground opacity-40" />
          </div>
        )}
        <div className="flex items-center justify-between">
          <div className="flex space-x-3 items-center">
            <Switch id="airplane-mode" onCheckedChange={toggleFilter} />
            <Label htmlFor="airplane-mode">Disease Filter</Label>
          </div>

          <div
            className={cn("flex space-x-4 transition-opacity items-center", {
              "opacity-0": !diseaseFilter,
            })}
          >
            <Label htmlFor="threshold">Threshold</Label>
            <Slider
              id="threshold"
              onValueChange={(v) => setThreshold(v[0])}
              min={0}
              max={100}
              step={0.5}
              className={cn("w-[360px] transition-opacity", {})}
            />
          </div>
        </div>
        <div className="flex space-x-3 items-center mt-0.5">
          <Switch
            id="ee"
            checked={detections}
            onCheckedChange={toggleDetections}
          />
          <Label htmlFor="airplane-mode">Leaf Detections</Label>
        </div>

        <div className="mt-8 mb-1.5 text-2xl text-left">Humidity</div>
        <div className="flex flex-col">
          <div className="flex justify-between text-sm text-muted-foreground font-medium mb-1.5">
            <div>Literally water</div>
            <div>Sahara Desert</div>
          </div>
          <Progress value={(sensorVal - 725) / 3} />
        </div>
        {/* <div>{sensorVal}</div> */}
      </div>
    </main>
  );
}

export default App;
