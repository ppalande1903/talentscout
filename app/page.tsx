"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { MessageCircle, User, Mail, Phone, MapPin, Code, Briefcase, Clock, Sparkles, Heart } from "lucide-react"

interface CandidateInfo {
  fullName: string
  email: string
  phone: string
  experienceYears: string
  desiredPosition: string
  location: string
  techStack: string[]
}

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

const CONVERSATION_STAGES = [
  "greeting",
  "name_collection",
  "email_collection",
  "phone_collection",
  "experience_collection",
  "position_collection",
  "location_collection",
  "tech_stack_collection",
  "technical_questions",
  "conclusion",
]

const TECH_KEYWORDS = [
  "python",
  "java",
  "javascript",
  "typescript",
  "react",
  "angular",
  "vue",
  "node.js",
  "django",
  "flask",
  "spring",
  "express",
  "mysql",
  "postgresql",
  "mongodb",
  "redis",
  "aws",
  "azure",
  "gcp",
  "docker",
  "kubernetes",
  "git",
]

const TECHNICAL_QUESTIONS = {
  python: [
    "What is the difference between list and tuple in Python?",
    "Explain Python's GIL (Global Interpreter Lock) and its implications.",
    "How do you handle exceptions in Python? Provide an example.",
  ],
  javascript: [
    "What is the difference between == and === in JavaScript?",
    "Explain closures in JavaScript with an example.",
    "What is the event loop in JavaScript and how does it work?",
  ],
  react: [
    "What is the difference between state and props in React?",
    "Explain the React component lifecycle methods.",
    "What are React Hooks and why are they useful?",
  ],
  general: [
    "Describe a challenging technical problem you've solved recently.",
    "How do you stay updated with new technologies in your field?",
    "What's your approach to debugging complex issues in your code?",
  ],
}

export default function TalentScoutAssistant() {
  const [messages, setMessages] = useState<Message[]>([])
  const [currentInput, setCurrentInput] = useState("")
  const [currentStageIndex, setCurrentStageIndex] = useState(0)
  const [candidateInfo, setCandidateInfo] = useState<CandidateInfo>({
    fullName: "",
    email: "",
    phone: "",
    experienceYears: "",
    desiredPosition: "",
    location: "",
    techStack: [],
  })
  const [technicalQuestions, setTechnicalQuestions] = useState<string[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [conversationStarted, setConversationStarted] = useState(false)
  const [conversationEnded, setConversationEnded] = useState(false)
  const [isTyping, setIsTyping] = useState(false)

  const validateEmail = (email: string): boolean => {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return pattern.test(email)
  }

  const validatePhone = (phone: string): boolean => {
    const digitsOnly = phone.replace(/\D/g, "")
    return digitsOnly.length >= 10 && digitsOnly.length <= 15
  }

  const extractTechStack = (input: string): string[] => {
    const found = TECH_KEYWORDS.filter((tech) => input.toLowerCase().includes(tech.toLowerCase()))
    return found.map((tech) => tech.charAt(0).toUpperCase() + tech.slice(1))
  }

  const generateTechnicalQuestions = (techStack: string[]): string[] => {
    const questions: string[] = []
    techStack.slice(0, 3).forEach((tech) => {
      const techLower = tech.toLowerCase()
      if (TECHNICAL_QUESTIONS[techLower as keyof typeof TECHNICAL_QUESTIONS]) {
        questions.push(...TECHNICAL_QUESTIONS[techLower as keyof typeof TECHNICAL_QUESTIONS].slice(0, 2))
      }
    })
    if (questions.length === 0) {
      questions.push(...TECHNICAL_QUESTIONS.general.slice(0, 3))
    }
    return questions.slice(0, 5)
  }

  const addMessage = (role: "user" | "assistant", content: string) => {
    setMessages((prev) => [...prev, { role, content, timestamp: new Date() }])
  }

  const simulateTyping = async (callback: () => void) => {
    setIsTyping(true)
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1000))
    setIsTyping(false)
    callback()
  }

  const handleResponse = async (userInput: string) => {
    if (!userInput.trim()) return

    addMessage("user", userInput)
    setCurrentInput("")

    const currentStage = CONVERSATION_STAGES[currentStageIndex]

    await simulateTyping(() => {
      let response = ""

      switch (currentStage) {
        case "greeting":
          response = `Hello! 👋 Welcome to TalentScout's AI Hiring Assistant!\n\nI'm here to help with your initial screening for technology positions. I'll gather some basic information about you and ask a few technical questions based on your expertise.\n\nThis should take about 5-10 minutes. Let's get started!\n\nWhat's your full name?`
          setCurrentStageIndex(1)
          break

        case "name_collection":
          if (userInput.trim()) {
            setCandidateInfo((prev) => ({ ...prev, fullName: userInput.trim() }))
            response = `Nice to meet you, ${userInput.trim()}! 😊\n\nCould you please provide your email address?`
            setCurrentStageIndex(2)
          } else {
            response = "Please provide your full name to continue."
          }
          break

        case "email_collection":
          if (validateEmail(userInput.trim())) {
            setCandidateInfo((prev) => ({ ...prev, email: userInput.trim() }))
            response = "Great! Now, what's your phone number?"
            setCurrentStageIndex(3)
          } else {
            response = "Please provide a valid email address (e.g., john@example.com)."
          }
          break

        case "phone_collection":
          if (validatePhone(userInput.trim())) {
            setCandidateInfo((prev) => ({ ...prev, phone: userInput.trim() }))
            response = "Perfect! How many years of professional experience do you have in technology?"
            setCurrentStageIndex(4)
          } else {
            response = "Please provide a valid phone number."
          }
          break

        case "experience_collection":
          if (userInput.trim()) {
            setCandidateInfo((prev) => ({ ...prev, experienceYears: userInput.trim() }))
            response =
              "Thanks! What position(s) are you interested in? (e.g., Software Developer, Data Scientist, DevOps Engineer)"
            setCurrentStageIndex(5)
          } else {
            response = "Please specify your years of experience."
          }
          break

        case "position_collection":
          if (userInput.trim()) {
            setCandidateInfo((prev) => ({ ...prev, desiredPosition: userInput.trim() }))
            response = "Excellent! What's your current location (city, state/country)?"
            setCurrentStageIndex(6)
          } else {
            response = "Please specify the position you're interested in."
          }
          break

        case "location_collection":
          if (userInput.trim()) {
            setCandidateInfo((prev) => ({ ...prev, location: userInput.trim() }))
            response = `Now for the technical part! 💻\n\nPlease tell me about your tech stack. List the programming languages, frameworks, databases, and tools you're proficient in.\n\nFor example: "Python, Django, React, PostgreSQL, AWS, Docker"`
            setCurrentStageIndex(7)
          } else {
            response = "Please provide your current location."
          }
          break

        case "tech_stack_collection":
          if (userInput.trim()) {
            const techStack = extractTechStack(userInput)
            if (techStack.length > 0) {
              setCandidateInfo((prev) => ({ ...prev, techStack }))
              const questions = generateTechnicalQuestions(techStack)
              setTechnicalQuestions(questions)
              response = `Perfect! I've identified your expertise in: ${techStack.join(", ")}\n\nNow I'll ask you ${questions.length} technical questions to assess your proficiency.\n\n**Question 1:** ${questions[0]}`
              setCurrentStageIndex(8)
            } else {
              response =
                "I couldn't identify specific technologies. Please mention specific programming languages, frameworks, or tools you know (e.g., Python, React, MySQL, etc.)."
            }
          } else {
            response = "Please tell me about your technical skills and tools you use."
          }
          break

        case "technical_questions":
          if (userInput.trim()) {
            const nextIndex = currentQuestionIndex + 1
            if (nextIndex < technicalQuestions.length) {
              setCurrentQuestionIndex(nextIndex)
              response = `Thank you for your answer! 👍\n\n**Question ${nextIndex + 1}:** ${technicalQuestions[nextIndex]}`
            } else {
              response = `Excellent! You've completed all the technical questions. 🎉\n\nThank you for taking the time to complete this screening! Our recruitment team will review your responses and contact you within 2-3 business days if your profile matches our current openings.\n\nIs there anything else you'd like to know about TalentScout or our process?`
              setCurrentStageIndex(9)
            }
          } else {
            response = "Please provide an answer to continue with the next question."
          }
          break

        default:
          response = `Thank you for your interest in TalentScout! 🌟\n\nYour information has been recorded and our team will be in touch soon.\n\nHave a wonderful day, and good luck with your job search!`
          setConversationEnded(true)
          break
      }

      addMessage("assistant", response)
    })
  }

  const startConversation = async () => {
    setConversationStarted(true)
    await simulateTyping(() => {
      const welcomeMessage = `Hello! 👋 Welcome to TalentScout's AI Hiring Assistant!\n\nI'm here to help with your initial screening for technology positions. I'll gather some basic information about you and ask a few technical questions based on your expertise.\n\nThis should take about 5-10 minutes. Let's get started!\n\nWhat's your full name?`
      addMessage("assistant", welcomeMessage)
      setCurrentStageIndex(1)
    })
  }

  const resetConversation = () => {
    setMessages([])
    setCurrentInput("")
    setCurrentStageIndex(0)
    setCandidateInfo({
      fullName: "",
      email: "",
      phone: "",
      experienceYears: "",
      desiredPosition: "",
      location: "",
      techStack: [],
    })
    setTechnicalQuestions([])
    setCurrentQuestionIndex(0)
    setConversationStarted(false)
    setConversationEnded(false)
  }

  const progress = (currentStageIndex / CONVERSATION_STAGES.length) * 100

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Cute animated background */}
      <div className="fixed inset-0 bg-gradient-to-br from-pink-100 via-purple-50 via-blue-50 via-green-50 to-yellow-50 animate-gradient-shift"></div>

      {/* Floating particles */}
      <div className="fixed inset-0 pointer-events-none">
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-3 h-3 rounded-full animate-float-${i % 4} opacity-60`}
            style={{
              left: `${10 + i * 8}%`,
              backgroundColor: ["#FFB6C1", "#87CEEB", "#DDA0DD", "#98FB98", "#F0E68C"][i % 5],
              animationDelay: `${i * 0.5}s`,
              animationDuration: `${4 + (i % 3)}s`,
            }}
          />
        ))}
      </div>

      {/* Header */}
      <div className="relative z-10 bg-gradient-to-r from-pink-200/80 to-purple-200/80 backdrop-blur-md text-gray-700 py-12 border-b border-white/20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 bg-clip-text text-transparent animate-pulse">
            🤖 TalentScout AI ✨
          </h1>
          <p className="text-xl opacity-90 font-medium">Your adorably smart partner for tech talent screening 💕</p>
        </div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="mb-6 bg-white/70 backdrop-blur-md border-pink-200/50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 rounded-3xl">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-purple-700">
                  <MessageCircle className="w-5 h-5 animate-bounce" />
                  About This Assistant
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  {[
                    { icon: "🎯", text: "AI-powered candidate screening" },
                    { icon: "🧠", text: "Intelligent question generation" },
                    { icon: "⚡", text: "Real-time conversation flow" },
                    { icon: "🔒", text: "Secure data handling" },
                  ].map((item, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-pink-50/50 transition-all duration-200 hover:scale-105"
                    >
                      <span className="text-lg animate-pulse">{item.icon}</span>
                      <span className="text-gray-600">{item.text}</span>
                    </div>
                  ))}
                </div>
                <div className="text-xs text-gray-500 bg-gradient-to-r from-pink-50 to-purple-50 p-3 rounded-xl border border-pink-200/30">
                  <strong className="text-purple-600">🔐 Privacy Notice:</strong> All data is handled securely and used
                  only for recruitment purposes.
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/70 backdrop-blur-md border-blue-200/50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 rounded-3xl">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-700">
                  <Clock className="w-5 h-5 animate-spin" />
                  Progress
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative">
                  <Progress
                    value={progress}
                    className="mb-3 h-3 bg-gradient-to-r from-pink-200 to-purple-200 rounded-full overflow-hidden"
                  />
                  <div
                    className="absolute top-0 left-0 h-3 bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 rounded-full transition-all duration-1000 ease-out animate-shimmer"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-600 font-medium">
                  Stage:{" "}
                  {CONVERSATION_STAGES[currentStageIndex]?.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                </p>
                <p className="text-xs text-gray-500 mt-1">{Math.round(progress)}% Complete</p>
              </CardContent>
            </Card>

            {candidateInfo.fullName && (
              <Card className="mt-6 bg-white/70 backdrop-blur-md border-green-200/50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 rounded-3xl">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-700">
                    <User className="w-5 h-5 animate-pulse" />
                    Candidate Info
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {candidateInfo.fullName && (
                    <div className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-green-50/50 transition-all duration-200">
                      <User className="w-4 h-4 text-green-500" />
                      <span className="font-medium">{candidateInfo.fullName}</span>
                    </div>
                  )}
                  {candidateInfo.email && (
                    <div className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-blue-50/50 transition-all duration-200">
                      <Mail className="w-4 h-4 text-blue-500" />
                      <span>{candidateInfo.email}</span>
                    </div>
                  )}
                  {candidateInfo.phone && (
                    <div className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-purple-50/50 transition-all duration-200">
                      <Phone className="w-4 h-4 text-purple-500" />
                      <span>{candidateInfo.phone}</span>
                    </div>
                  )}
                  {candidateInfo.location && (
                    <div className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-pink-50/50 transition-all duration-200">
                      <MapPin className="w-4 h-4 text-pink-500" />
                      <span>{candidateInfo.location}</span>
                    </div>
                  )}
                  {candidateInfo.desiredPosition && (
                    <div className="flex items-center gap-3 text-sm p-2 rounded-xl hover:bg-yellow-50/50 transition-all duration-200">
                      <Briefcase className="w-4 h-4 text-yellow-600" />
                      <span>{candidateInfo.desiredPosition}</span>
                    </div>
                  )}
                  {candidateInfo.techStack.length > 0 && (
                    <div className="mt-4">
                      <div className="flex items-center gap-2 text-sm mb-3 font-medium text-gray-700">
                        <Code className="w-4 h-4 text-indigo-500" />
                        Tech Stack:
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {candidateInfo.techStack.map((tech, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="text-xs bg-gradient-to-r from-pink-200 to-purple-200 text-purple-700 border-none hover:scale-110 transition-transform duration-200 cursor-default rounded-full px-3 py-1"
                          >
                            {tech}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <Card className="h-[600px] flex flex-col bg-white/70 backdrop-blur-md border-pink-200/50 shadow-xl rounded-3xl overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-pink-100/50 to-purple-100/50 border-b border-pink-200/30">
                <CardTitle className="flex items-center gap-2 text-purple-700">
                  💬 Chat Interface
                  <Sparkles className="w-5 h-5 animate-pulse text-pink-500" />
                </CardTitle>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col p-6">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-2xl transition-all duration-300 hover:scale-[1.02] ${
                        message.role === "user"
                          ? "bg-gradient-to-r from-pink-100/80 to-rose-100/80 border-l-4 border-pink-400 ml-8 hover:shadow-lg"
                          : "bg-gradient-to-r from-purple-100/80 to-blue-100/80 border-l-4 border-purple-400 mr-8 hover:shadow-lg"
                      }`}
                    >
                      <div className="font-semibold mb-2 flex items-center gap-2">
                        {message.role === "user" ? (
                          <>
                            <span className="text-pink-600">👤 You</span>
                            <Heart className="w-4 h-4 text-pink-400 animate-pulse" />
                          </>
                        ) : (
                          <>
                            <span className="text-purple-600">🤖 Assistant</span>
                            <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" />
                          </>
                        )}
                      </div>
                      <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">{message.content}</div>
                      <div className="text-xs text-gray-500 mt-2 text-right">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  ))}

                  {isTyping && (
                    <div className="bg-gradient-to-r from-purple-100/80 to-blue-100/80 border-l-4 border-purple-400 mr-8 p-4 rounded-2xl">
                      <div className="font-semibold mb-2 flex items-center gap-2">
                        <span className="text-purple-600">🤖 Assistant</span>
                        <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" />
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="flex space-x-1">
                          {[0, 1, 2].map((i) => (
                            <div
                              key={i}
                              className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                              style={{ animationDelay: `${i * 0.1}s` }}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-purple-600 animate-pulse">Typing...</span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Input Area */}
                {!conversationStarted ? (
                  <Button
                    onClick={startConversation}
                    className="w-full bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 hover:from-pink-500 hover:via-purple-500 hover:to-blue-500 text-white font-semibold py-4 px-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 hover:scale-105 animate-pulse"
                    size="lg"
                  >
                    🚀 Start Magical Screening Process ✨
                  </Button>
                ) : conversationEnded ? (
                  <div className="space-y-4">
                    <div className="text-center p-6 bg-gradient-to-r from-green-100/80 to-emerald-100/80 rounded-2xl border-2 border-green-200/50 shadow-lg">
                      <h3 className="font-bold text-green-700 mb-2 text-lg flex items-center justify-center gap-2">
                        🎉 Conversation Completed!
                        <Sparkles className="w-5 h-5 animate-pulse" />
                      </h3>
                      <p className="text-green-600">Thank you for using TalentScout's AI Hiring Assistant! 💕</p>
                    </div>
                    <Button
                      onClick={resetConversation}
                      variant="outline"
                      className="w-full bg-white/50 border-2 border-pink-300 text-pink-700 hover:bg-pink-50 hover:border-pink-400 rounded-2xl py-3 transition-all duration-300 hover:-translate-y-1 hover:scale-105"
                    >
                      🔄 Start New Magical Conversation ✨
                    </Button>
                  </div>
                ) : (
                  <div className="flex gap-3">
                    <Input
                      value={currentInput}
                      onChange={(e) => setCurrentInput(e.target.value)}
                      placeholder="Type your response here... ✨"
                      onKeyPress={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault()
                          handleResponse(currentInput)
                        }
                      }}
                      disabled={isTyping}
                      className="flex-1 rounded-2xl border-2 border-pink-200 focus:border-pink-400 focus:ring-pink-300 bg-white/80 backdrop-blur-sm"
                    />
                    <Button
                      onClick={() => handleResponse(currentInput)}
                      disabled={!currentInput.trim() || isTyping}
                      className="bg-gradient-to-r from-pink-400 to-purple-400 hover:from-pink-500 hover:to-purple-500 text-white rounded-2xl px-6 transition-all duration-300 hover:-translate-y-1 hover:scale-105 shadow-lg hover:shadow-xl"
                    >
                      Send 💕
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative z-10 bg-gradient-to-r from-pink-100/80 to-purple-100/80 backdrop-blur-md py-8 mt-12 border-t border-white/20">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-lg font-bold mb-2 bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent flex items-center justify-center gap-2">
            🏢 TalentScout - Connecting Tech Talent with Opportunities
            <Heart className="w-5 h-5 text-pink-500 animate-pulse" />
          </h3>
          <p className="text-sm text-gray-600">Built with python and streamlit • Powered by AI • Made with 💕</p>
        </div>
      </footer>

      <style jsx>{`
        @keyframes gradient-shift {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        
        @keyframes float-0 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        @keyframes float-1 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-30px) rotate(180deg); }
        }
        
        @keyframes float-2 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-25px) rotate(180deg); }
        }
        
        @keyframes float-3 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-35px) rotate(180deg); }
        }
        
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
        
        .animate-gradient-shift {
          background-size: 400% 400%;
          animation: gradient-shift 15s ease infinite;
        }
        
        .animate-float-0 { animation: float-0 4s ease-in-out infinite; }
        .animate-float-1 { animation: float-1 5s ease-in-out infinite; }
        .animate-float-2 { animation: float-2 6s ease-in-out infinite; }
        .animate-float-3 { animation: float-3 7s ease-in-out infinite; }
        
        .animate-shimmer {
          background-size: 200% 100%;
          animation: shimmer 2s infinite;
        }
      `}</style>
    </div>
  )
}
