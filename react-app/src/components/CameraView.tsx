import { useEffect, useRef, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";

type CameraInfo = {
  id: string;
  label: string;
};

function CameraFeed() {
  const videoRef = useRef(null);

  // const [selectedCamera, setSelectedCamera] = useState<CameraInfo | null>(null);
  const [cameraOpts, setCameraOpts] = useState<CameraInfo[]>();

  useEffect(() => {
    // Get access to the camera
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          // Attach the video stream to the video element and autoplay
          const video = videoRef.current as HTMLVideoElement | null;
          if (!video) return;

          video.srcObject = stream;
          video.play();
        })
        .catch((error) => {
          console.error("Error accessing the camera:", error);
        });
    }
  }, []);

  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then((devices) => {
      const cameraDevices = devices
        .filter((d) => d.kind === "videoinput")
        .map((d) => ({
          id: d.deviceId,
          label: d.label ?? `Camera ${d.deviceId}`,
        }));

      console.log(cameraDevices);

      setCameraOpts(cameraDevices);
    });
  }, []);

  function setCamera(deviceId: string) {
    navigator.mediaDevices
      .getUserMedia({ video: { deviceId } })
      .then((stream) => {
        // Attach the video stream to the video element and autoplay
        const video = videoRef.current as HTMLVideoElement | null;
        if (!video) return;

        video.srcObject = stream;
        video.play();
      })
      .catch((error) => {
        console.error("Error accessing the camera:", error);
      });
  }

  return (
    <div className="flex flex-col gap-4">
      <video
        ref={videoRef}
        width="640"
        height="480"
        className="border rounded-md"
      />

      <Select
        onValueChange={(v) => {
          setCamera(v);
        }}
      >
        <SelectTrigger className="w-[360px]">
          <SelectValue placeholder="Switch Cameras..." />
        </SelectTrigger>
        <SelectContent>
          {cameraOpts?.map((opt) => (
            <SelectItem value={opt.id}>{opt.label}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

export default CameraFeed;
