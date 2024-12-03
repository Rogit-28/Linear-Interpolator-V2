"use client"

import { useState, useEffect, useCallback } from "react"
import { X, Minus, Square, Move3D } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Checkbox } from "@/components/ui/checkbox"
import { cn } from "@/lib/utils"

interface ScalingRangeModalProps {
  isOpen?: boolean
  onClose?: () => void
  onChange?: (data: ScalingRangeData) => void
}

interface ScalingRangeData {
  x1: string
 x2: string
  y1: string
  y2: string
  z1: string
  z2: string
  selectedAxis: "x" | "y" | "z"
  axisValues: { x: string; y: string; z: string }
  zInHex: boolean
}

interface HistoryEntry {
  timestamp: string;
  x1: string;
  x2: string;
  y1: string;
  y2: string;
  z1: string;
  z2: string;
  inputAxis: string;
  inputValue: string;
  outputX: string;
  outputY: string;
  outputZ: string;
  selectedAxis: "x" | "y" | "z";
  zInHex: boolean;
}

const HISTORY_KEY = 'scaling_history';
const MAX_HISTORY_ENTRIES = 100;

interface ScalingRequest {
  x_input: string
  y_input: string
  z_input: string
  x1: string
  x2: string
  y1: string
  y2: string
  z1: string
  z2: string
  scale_from: string
  z_in_hex: boolean
}

interface ScalingResponse {
  x: string
  y: string
  z: string
}

export function ScalingRangeModal({ isOpen = true, onClose, onChange }: ScalingRangeModalProps) {
  const [rangeValues, setRangeValues] = useState({
    x1: "",
    x2: "",
    y1: "",
    y2: "",
    z1: "",
    z2: "",
  })

  const [selectedAxis, setSelectedAxis] = useState<"x" | "y" | "z">("x")
  const [axisValues, setAxisValues] = useState({ x: "", y: "", z: "" })
  const [zInHex, setZInHex] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [activeTab, setActiveTab] = useState<"calculator" | "history">("calculator")
  const [debounceTimer, setDebounceTimer] = useState<NodeJS.Timeout | null>(null)

  const triggerChange = (
    updates: Partial<{
      rangeValues: typeof rangeValues
      selectedAxis: "x" | "y" | "z"
      axisValues: typeof axisValues
      zInHex: boolean
    }>,
  ) => {
    const newData: ScalingRangeData = {
      ...(updates.rangeValues ?? rangeValues),
      selectedAxis: updates.selectedAxis ?? selectedAxis,
      axisValues: updates.axisValues ?? axisValues,
      zInHex: updates.zInHex ?? zInHex,
    }
    onChange?.(newData)
  }

 const handleRangeChange = (key: keyof typeof rangeValues, value: string) => {
    const newRangeValues = { ...rangeValues, [key]: value }
    setRangeValues(newRangeValues)
    triggerChange({ rangeValues: newRangeValues })
  }

  const handleAxisSelect = (axis: "x" | "y" | "z") => {
    setSelectedAxis(axis)
    triggerChange({ selectedAxis: axis })
  }

   const performScalingCalculation = useCallback(async (currentAxisValues: { x: string; y: string; z: string }) => {
    if (isLoading) return
    
    // Check if there's a valid input value for the selected axis
    const inputValue = currentAxisValues[selectedAxis];
    const hasValidInput = inputValue !== "" && !isNaN(parseFloat(inputValue));
    
    if (!hasValidInput) {
      // If no valid input, clear results
      setAxisValues({ x: "", y: "", z: "" });
      triggerChange({ axisValues: { x: "", y: "", z: "" } });
      return;
    }

    setIsLoading(true)
    
    try {
      // Send all available range values - the backend will handle partial data
      // The backend only uses the ranges that are relevant to the selected axis
      const request: ScalingRequest = {
        x_input: currentAxisValues.x || "",
        y_input: currentAxisValues.y || "",
        z_input: currentAxisValues.z || "",
        x1: rangeValues.x1,
        x2: rangeValues.x2,
        y1: rangeValues.y1,
        y2: rangeValues.y2,
        z1: rangeValues.z1,
        z2: rangeValues.z2,
        scale_from: selectedAxis,
        z_in_hex: zInHex
      }

      const response = await fetch("http://127.0.0.1:8001/scale", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      })

      if (response.ok) {
        const result: ScalingResponse = await response.json()
        setAxisValues(result)
        triggerChange({ axisValues: result })
        
        // Log to history after successful calculation
        logToHistory(inputValue, result);
      } else {
        const errorText = await response.text()
        console.error("Scaling calculation failed:", errorText)
        
        // Handle partial results - if we get an error, we can still show what's calculable
        // For now, let's clear the results to indicate an issue
        setAxisValues({ x: "", y: "", z: "" });
      }
    } catch (error) {
      console.error("Error calling scaling API:", error)
      setAxisValues({ x: "", y: "", z: "" });
    } finally {
      setIsLoading(false)
    }
  }, [rangeValues, selectedAxis, zInHex, isLoading, triggerChange])

  const logToHistory = (inputValue: string, outputs: ScalingResponse) => {
    const newEntry: HistoryEntry = {
      timestamp: new Date().toISOString(),
      x1: rangeValues.x1 || "-",
      x2: rangeValues.x2 || "-",
      y1: rangeValues.y1 || "-",
      y2: rangeValues.y2 || "-",
      z1: rangeValues.z1 || "-",
      z2: rangeValues.z2 || "-",
      inputAxis: selectedAxis,
      inputValue: inputValue,
      outputX: outputs.x,
      outputY: outputs.y,
      outputZ: outputs.z,
      selectedAxis: selectedAxis,
      zInHex: zInHex
    };

    const updatedHistory = [newEntry, ...history];
    
    // Keep only the last 100 entries
    if (updatedHistory.length > MAX_HISTORY_ENTRIES) {
      updatedHistory.splice(MAX_HISTORY_ENTRIES);
    }

    setHistory(updatedHistory);
    
    // Save to localStorage
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updatedHistory));
  }

  const loadHistoryFromStorage = () => {
    try {
      const storedHistory = localStorage.getItem(HISTORY_KEY);
      if (storedHistory) {
        const parsedHistory: HistoryEntry[] = JSON.parse(storedHistory);
        setHistory(parsedHistory);
      }
    } catch (error) {
      console.error("Error loading history from storage:", error);
      setHistory([]);
    }
  }

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem(HISTORY_KEY);
  }

  const handleAxisValueChange = (axis: string, value: string) => {
    const newAxisValues = { ...axisValues, [axis]: value }
    setAxisValues(newAxisValues)
    triggerChange({ axisValues: newAxisValues })
  }

  const handleAxisKeyDown = (axis: string, value: string, event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      performScalingCalculation(axisValues)
    }
  }

  const handleRangeKeyDown = (axis: string, position: string, event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      performScalingCalculation(axisValues)
    }
  }

  const handleManualCalculate = () => {
    performScalingCalculation(axisValues)
 }

  const handleHexChange = (checked: boolean) => {
    setZInHex(checked)
    triggerChange({ zInHex: checked })
    // Trigger recalculation when hex setting changes
    performScalingCalculation(axisValues)
  }

  // Update calculations when selected axis or zInHex changes
  useEffect(() => {
    performScalingCalculation(axisValues)
  }, [selectedAxis, zInHex])

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer) {
        clearTimeout(debounceTimer)
      }
    }
  }, [])

  // Load history from localStorage on initial render
  useEffect(() => {
    loadHistoryFromStorage();
  }, []);

  if (!isOpen) return null

  const axisConfig = [
    { key: "x", label: "X", color: "text-sky-400", borderColor: "border-sky-500", bgColor: "bg-sky-500/10" },
    {
      key: "y",
      label: "Y",
      color: "text-emerald-400",
      borderColor: "border-emerald-500",
      bgColor: "bg-emerald-500/10",
    },
    { key: "z", label: "Z", color: "text-amber-400", borderColor: "border-amber-500", bgColor: "bg-amber-500/10" },
  ] as const

 return (
    <div className="fixed inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm z-50">
      <div className="w-full max-w-xl bg-card border border-border rounded-xl shadow-2xl overflow-hidden animate-in fade-in-0 zoom-in-95 duration-200">
        {/* Title Bar */}
        <div className="flex items-center justify-between px-4 py-2.5 bg-secondary/50 border-b border-border">
          <div className="flex items-center gap-2.5">
            <div className="flex items-center justify-center w-7 h-7 rounded-md bg-primary/20">
              <Move3D className="w-3.5 h-3.5 text-primary" />
            </div>
            <h2 className="text-sm font-medium text-foreground">Scaling Range</h2>
          </div>
          <div className="flex items-center gap-0.5">
            <button className="p-1.5 rounded-md hover:bg-muted transition-colors text-muted-foreground hover:text-foreground">
              <Minus className="w-3.5 h-3.5" />
            </button>
            <button className="p-1.5 rounded-md hover:bg-muted transition-colors text-muted-foreground hover:text-foreground">
              <Square className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-md hover:bg-destructive/20 transition-colors text-muted-foreground hover:text-destructive"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-border">
          <button
            className={cn(
              "flex-1 py-2 text-sm font-medium transition-colors",
              activeTab === "calculator" 
                ? "text-foreground border-b-2 border-primary" 
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setActiveTab("calculator")}
          >
            Calculator
          </button>
          <button
            className={cn(
              "flex-1 py-2 text-sm font-medium transition-colors",
              activeTab === "history" 
                ? "text-foreground border-b-2 border-primary" 
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setActiveTab("history")}
          >
            History ({history.length}/100)
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-5">
          {/* Calculator Tab */}
          {activeTab === "calculator" && (
            <div className="space-y-2.5">
              {axisConfig.map((axis) => (
                <div key={axis.key} className="grid grid-cols-2 gap-3">
                  {/* Range inputs */}
                  <div className="flex items-center gap-2 p-2.5 rounded-lg bg-secondary/30 border-border">
                    <span className={cn("text-xs font-semibold w-4 shrink-0", axis.color)}>{axis.label}1</span>
                    <Input
                      type="text"
                      placeholder="min"
                      value={rangeValues[`${axis.key}1` as keyof typeof rangeValues]}
                      onChange={(e) => handleRangeChange(`${axis.key}1` as keyof typeof rangeValues, e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          performScalingCalculation(axisValues)
                        }
                      }}
                      className={cn("flex-1 h-8 text-sm bg-background/50 border-border")}
                    />
                    <span className={cn("text-xs font-semibold w-4 shrink-0", axis.color)}>{axis.label}2</span>
                    <Input
                      type="text"
                      placeholder="max"
                      value={rangeValues[`${axis.key}2` as keyof typeof rangeValues]}
                      onChange={(e) => handleRangeChange(`${axis.key}2` as keyof typeof rangeValues, e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          performScalingCalculation(axisValues)
                        }
                      }}
                      className={cn("flex-1 h-8 text-sm bg-background/50 border-border")}
                    />
                  </div>

                  {/* Axis selection */}
                  <div
                    className={cn(
                      "flex items-center gap-2 p-2.5 rounded-lg border transition-all cursor-pointer",
                      selectedAxis === axis.key
                        ? cn(axis.bgColor, axis.borderColor)
                        : "bg-secondary/30 border-border hover:border-muted-foreground/50",
                    )}
                    onClick={() => handleAxisSelect(axis.key)}
                  >
                    <RadioGroup value={selectedAxis} onValueChange={(val) => handleAxisSelect(val as "x" | "y" | "z")}>
                      <RadioGroupItem
                        value={axis.key}
                        id={axis.key}
                        className={cn("border-2 shrink-0", selectedAxis === axis.key && axis.borderColor)}
                      />
                    </RadioGroup>
                    <Label
                      htmlFor={axis.key}
                      className={cn("text-xs font-semibold w-4 shrink-0 cursor-pointer", axis.color)}
                    >
                      {axis.label}
                    </Label>
                    <Input
                      type="text"
                      placeholder={axis.label}
                      value={axisValues[axis.key]}
                      onChange={(e) => handleAxisValueChange(axis.key, e.target.value)}
                      onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => handleAxisKeyDown(axis.key, e.currentTarget.value, e)}
                      className="flex-1 h-8 text-sm bg-background/50 border-border"
                      onClick={(e) => e.stopPropagation()}
                      disabled={isLoading}
                    />
                  </div>
                </div>
              ))}
              {/* Controls Row - Z in Hex checkbox on left, Calculate button on right */}
              <div className="flex items-center justify-between pt-2">
                <div className="flex items-center gap-2">
                  <Checkbox
                    id="z-in-hex"
                    checked={zInHex}
                    onCheckedChange={handleHexChange}
                    disabled={isLoading}
                  />
                  <Label htmlFor="z-in-hex" className="text-sm text-foreground">
                    Z in Hex
                  </Label>
                </div>
                <button
                  onClick={handleManualCalculate}
                  disabled={isLoading}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? "Calculating..." : "Calculate"}
                </button>
              </div>
            </div>
          )}

          {/* History Tab */}
          {activeTab === "history" && (
            <div className="space-y-3">
              {history.length > 0 ? (
                <>
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium text-foreground">Calculation History</h3>
                    <button
                      onClick={clearHistory}
                      className="px-3 py-1 text-xs rounded-md bg-destructive/20 hover:bg-destructive/30 text-destructive transition-colors"
                    >
                      Clear All
                    </button>
                  </div>
                  <div className="max-h-60 overflow-y-auto border border-border rounded-lg">
                    <table className="w-full text-xs">
                      <thead className="bg-secondary/30 sticky top-0">
                        <tr>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-20">Time</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">x1</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">x2</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">y1</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">y2</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">z1</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">z2</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">X</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">Y</th>
                          <th className="px-2 py-1 text-left font-medium text-muted-foreground w-16">Z</th>
                        </tr>
                      </thead>
                      <tbody>
                        {history.slice(0, 50).map((entry, index) => (
                          <tr key={index} className="border-t border-border/50 hover:bg-secondary/20">
                            <td className="px-2 py-1 font-mono text-xs">{new Date(entry.timestamp).toLocaleTimeString()}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.x1}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.x2}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.y1}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.y2}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.z1}</td>
                            <td className="px-2 py-1 text-blue-600 font-medium">{entry.z2}</td>
                            <td className={cn("px-2 py-1 font-medium", 
                              entry.selectedAxis === 'x' ? "text-red-500" : "text-green-600")}>
                              {entry.outputX}
                            </td>
                            <td className={cn("px-2 py-1 font-medium", 
                              entry.selectedAxis === 'y' ? "text-red-500" : "text-green-600")}>
                              {entry.outputY}
                            </td>
                            <td className={cn("px-2 py-1 font-medium", 
                              entry.selectedAxis === 'z' ? "text-red-500" : "text-green-600")}>
                              {entry.outputZ}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No calculation history yet.</p>
                  <p className="text-xs mt-1">Perform calculations to see them listed here.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
 )
}
