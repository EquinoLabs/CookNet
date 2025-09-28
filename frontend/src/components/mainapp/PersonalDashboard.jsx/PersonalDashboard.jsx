import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Input,
  Image,
  Avatar,
  Chip,
  Progress,
  Divider
} from "@heroui/react";

const posts = [
  { id: 1, title: "Spaghetti Carbonara", image: "https://via.placeholder.com/300x200" },
  { id: 2, title: "Vegan Tacos", image: "https://via.placeholder.com/300x200" },
  { id: 3, title: "Chocolate Cake", image: "https://via.placeholder.com/300x200" },
];

export default function PersonalDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-100 p-12">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 mb-16">
          <div className="flex flex-col gap-3">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Dashboard
            </h1>
            <p className="text-base text-slate-600">Welcome back, Lakshya! Here's what's happening today.</p>
          </div>
          <Avatar
            src="https://via.placeholder.com/80"
            className="w-20 h-20 text-large ring-4 ring-white shadow-2xl"
          />
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-8 mb-20">
          
          {/* Stat Card 1 */}
          <Card className="bg-white/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <CardBody className="flex flex-col items-center justify-center gap-4 p-8">
              <div className="text-2xl">💬</div>
              <div className="flex flex-col items-center gap-2">
                <span className="text-lg font-bold text-blue-600">42</span>
                <span className="text-sm font-medium text-slate-500 text-center">Replies Posted</span>
              </div>
            </CardBody>
          </Card>

          {/* Stat Card 2 */}
          <Card className="bg-white/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <CardBody className="flex flex-col items-center justify-center gap-4 p-8">
              <div className="text-2xl">🔄</div>
              <div className="flex flex-col items-center gap-2">
                <span className="text-lg font-bold text-emerald-600">18</span>
                <span className="text-sm font-medium text-slate-500 text-center">Total Recreations</span>
              </div>
            </CardBody>
          </Card>

          {/* Stat Card 3 */}
          <Card className="bg-white/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <CardBody className="flex flex-col items-center justify-center gap-4 p-8">
              <div className="text-2xl">👥</div>
              <div className="flex flex-col items-center gap-2">
                <span className="text-lg font-bold text-purple-600">256</span>
                <span className="text-sm font-medium text-slate-500 text-center">New Followers</span>
              </div>
            </CardBody>
          </Card>

          {/* Stat Card 4 */}
          <Card className="bg-white/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <CardBody className="flex flex-col items-center justify-center gap-4 p-8">
              <div className="text-2xl">📈</div>
              <div className="flex flex-col items-center gap-2">
                <span className="text-lg font-bold text-orange-600">74</span>
                <span className="text-sm font-medium text-slate-500 text-center">Community Activity</span>
              </div>
            </CardBody>
          </Card>

          {/* AI Recommendations Card */}
          <Card className="bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 xl:col-span-1 sm:col-span-2 lg:col-span-2">
            <CardHeader className="flex gap-3 p-8">
              <div className="text-lg">🤖</div>
              <div className="flex flex-col">
                <p className="text-base font-bold">AI Recommendations</p>
              </div>
            </CardHeader>
            <Divider className="bg-white/20"/>
            <CardBody className="flex flex-col gap-4 p-8">
              <div className="flex items-center gap-4 p-4 bg-white/20 rounded-xl backdrop-blur-sm">
                <span className="text-base">🍜</span>
                <span className="font-medium text-sm">Try Vegan Ramen</span>
              </div>
              <div className="flex items-center gap-4 p-4 bg-white/20 rounded-xl backdrop-blur-sm">
                <span className="text-base">🍰</span>
                <span className="font-medium text-sm">Join Dessert Week</span>
              </div>
              <div className="flex items-center gap-4 p-4 bg-white/20 rounded-xl backdrop-blur-sm">
                <span className="text-base">🌿</span>
                <span className="font-medium text-sm">Cook with 5 ingredients</span>
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 mb-20">
          
          {/* Recipes Section */}
          <div className="lg:col-span-2">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 mb-10">
              <h2 className="text-xl font-bold text-slate-800">Your Recipes</h2>
              <Button 
                color="primary" 
                variant="shadow"
                size="md"
                className="px-6 py-2 font-medium text-sm"
              >
                + Add Recipe
              </Button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              {posts.map((post) => (
                <Card 
                  key={post.id} 
                  className="bg-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1"
                  isHoverable
                  isPressable
                >
                  <CardHeader className="p-0">
                    <Image
                      alt={post.title}
                      className="object-cover w-full h-56"
                      src={post.image}
                    />
                  </CardHeader>
                  <CardBody className="flex flex-col gap-4 p-8">
                    <h3 className="text-base font-bold text-slate-800">{post.title}</h3>
                  </CardBody>
                  <Divider/>
                  <CardFooter className="flex gap-4 p-8">
                    <Button 
                      color="primary" 
                      variant="flat"
                      size="sm"
                      className="flex-1 font-medium py-2 text-sm"
                    >
                      Edit
                    </Button>
                    <Button 
                      color="danger" 
                      variant="light"
                      size="sm"
                      className="flex-1 font-medium py-2 text-sm"
                    >
                      Delete
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </div>

          {/* Sidebar */}
          <div className="flex flex-col gap-10">
            
            {/* Engagement Card */}
            <Card className="bg-white shadow-xl">
              <CardHeader className="flex gap-3 p-8">
                <div className="text-base">📊</div>
                <div className="flex flex-col">
                  <p className="text-base font-bold text-slate-800">Engagement Overview</p>
                </div>
              </CardHeader>
              <Divider/>
              <CardBody className="flex flex-col items-center justify-center gap-6 p-12">
                <div className="text-4xl text-slate-300">📊</div>
                <p className="text-sm font-medium text-slate-500">Chart Coming Soon</p>
              </CardBody>
            </Card>

            {/* Challenge Card */}
            <Card className="bg-white shadow-xl">
              <CardHeader className="flex gap-3 p-8">
                <div className="text-base">🏆</div>
                <div className="flex flex-col">
                  <p className="text-base font-bold text-slate-800">Active Challenges</p>
                </div>
              </CardHeader>
              <Divider/>
              <CardBody className="flex flex-col items-center justify-center gap-6 p-12">
                <div className="w-24 h-24 bg-gradient-to-br from-yellow-100 to-orange-200 rounded-full flex items-center justify-center border-4 border-dashed border-orange-300">
                  <span className="text-2xl">🥧</span>
                </div>
                <div className="flex flex-col items-center gap-4 w-full">
                  <p className="text-sm font-semibold text-slate-700">Pie Week Challenge</p>
                  <Progress
                    value={65}
                    color="warning"
                    size="md"
                    className="w-full"
                  />
                  <p className="text-xs text-slate-500">3 of 5 completed</p>
                </div>
              </CardBody>
            </Card>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-12">
          
          {/* Notifications Card */}
          <Card className="bg-white shadow-xl">
            <CardHeader className="flex gap-3 p-8">
              <div className="text-base">🔔</div>
              <div className="flex flex-col">
                <p className="text-base font-bold text-slate-800">Recent Activity</p>
              </div>
            </CardHeader>
            <Divider/>
            <CardBody className="flex flex-col gap-6 p-8">
              <div className="flex items-start gap-4 p-6 bg-emerald-50 rounded-xl border-l-4 border-emerald-400">
                <Chip color="success" variant="flat" size="sm">New</Chip>
                <div className="flex flex-col gap-2">
                  <p className="text-sm font-semibold text-slate-700">🎉 You gained 20 new followers</p>
                  <p className="text-xs text-slate-500">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-6 bg-orange-50 rounded-xl border-l-4 border-orange-400">
                <Chip color="warning" variant="flat" size="sm">Hot</Chip>
                <div className="flex flex-col gap-2">
                  <p className="text-sm font-semibold text-slate-700">🔥 Your recipe was recreated 5 times</p>
                  <p className="text-xs text-slate-500">5 hours ago</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-6 bg-blue-50 rounded-xl border-l-4 border-blue-400">
                <Chip color="primary" variant="flat" size="sm">Event</Chip>
                <div className="flex flex-col gap-2">
                  <p className="text-sm font-semibold text-slate-700">🍴 New challenge: "Street Food Week"</p>
                  <p className="text-xs text-slate-500">1 day ago</p>
                </div>
              </div>
            </CardBody>
          </Card>

          {/* Settings Card */}
          <Card className="bg-white shadow-xl">
            <CardHeader className="flex gap-3 p-8">
              <div className="text-base">⚙️</div>
              <div className="flex flex-col">
                <p className="text-base font-bold text-slate-800">Quick Settings</p>
              </div>
            </CardHeader>
            <Divider/>
            <CardBody className="flex flex-col gap-8 p-8">
              <Input
                type="text"
                label="Display Name"
                placeholder="Enter your name"
                defaultValue="Lakshya"
                variant="bordered"
                size="md"
                classNames={{
                  base: "max-w-full",
                  mainWrapper: "h-full",
                  input: "text-sm",
                  inputWrapper: "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20"
                }}
              />
              <Input
                type="text"
                label="Bio"
                placeholder="Tell us about yourself"
                defaultValue="Food explorer & home chef"
                variant="bordered"
                size="md"
                classNames={{
                  base: "max-w-full",
                  mainWrapper: "h-full",
                  input: "text-sm",
                  inputWrapper: "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20"
                }}
              />
              <Input
                type="text"
                label="Diet Preference"
                placeholder="Your diet preference"
                defaultValue="Vegetarian"
                variant="bordered"
                size="md"
                classNames={{
                  base: "max-w-full",
                  mainWrapper: "h-full",
                  input: "text-sm",
                  inputWrapper: "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20"
                }}
              />
            </CardBody>
            <Divider/>
            <CardFooter className="p-8">
              <Button 
                color="primary" 
                variant="shadow"
                size="md"
                className="w-full font-medium py-3 text-sm"
              >
                Save Changes
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
