#Simulate an income statement and visualize it in 3D
import vtk
import time
import imageio


time_scale = "weekly"  # Time scale (you can set it to your desired timescale)

# Function to create a sphere with a given radius
def create_sphere(radius, color, position):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.SetPosition(position[0], position[1], position[2])  # Set position for the actor

    return actor

def update_revenue_and_expenses(debt, revenue, expenses, iteration, time_scale):
    
    apr = 0.25  # Annual Percentage Rate
    monthly_apr = apr / 12  # Monthly interest rate
    daily_apr = monthly_apr/30
    weekly_apr = daily_apr * 7
    hourly_apr = daily_apr/8
    minute_apr = hourly_apr/60
    second_apr = minute_apr/60
    hourly_rate = 26
    minute_rate = hourly_rate/60
    second_rate = minute_rate/60
    
    if time_scale == "yearly":
        debt += apr * debt
        revenue += hourly_rate * 10080
        expenses += hourly_rate * 10080
        debt_service = .8 * hourly_rate * 10080
        debt -= debt_service

    if time_scale == "monthly":
        debt += monthly_apr * debt  # Increase the debt by monthly interest
        revenue += hourly_rate * 160
        expenses += 0.8 * hourly_rate * 160  # Increase expenses by 80% of revenue
        debt_service = .8 * hourly_rate * 160  # Assume 80% of revenue used to pay debt
        debt -= debt_service  # Decrease the debt by the debt service
        
        
    if time_scale == "daily":
        debt += daily_apr * debt  # Increase the debt by the daily interest
        revenue += hourly_rate * 8  # Increment revenue by a fixed amount
        expenses += .8 * hourly_rate * 8  # Increment expenses by a fixed amount
        debt_service = .8 * hourly_rate * 8  # Use expenses to pay down the debt
        debt -= debt_service  # Decrease the debt by the debt service

        
    if time_scale == "weekly":
        debt += weekly_apr * debt
        revenue += hourly_rate * 80
        expenses += .8 * hourly_rate * 80
        debt_service = .8 * hourly_rate * 80  # Assume 80% of revenue used to pay debt
        debt -= debt_service  # Decrease the debt by the debt service
        
        
    if time_scale == "hourly":
        debt += hourly_apr * debt
        revenue += hourly_rate
        expenses += .8 * hourly_rate
        debt_service = .8 * hourly_rate  # Assume 80% of revenue used to pay debt
        debt -= debt_service  # Decrease the debt by the debt service
                
        
    if time_scale == "second":
        debt += second_apr * debt
        revenue += second_rate 
        expenses += .8 * second_rate
        debt_service = .8 * second_rate  # Assume 80% of revenue used to pay debt
        debt -= debt_service  # Decrease the debt by the debt service
                
        
    if time_scale == "minute":
        debt += minute_apr * debt
        revenue += minute_rate
        expenses += .8 * minute_rate
        debt_service = .8 * minute_rate  # Assume 80% of revenue used to pay debt
        debt -= debt_service  # Decrease the debt by the debt service
                
        


    net_income = revenue - expenses
    return debt, revenue, expenses, net_income

# Initialize variables
debt = 100000  # Initial debt value
revenue = 0
expenses = 0
#debt_service = .8 * revenue
#debt -= debt_service
#how does debt_service change according to time scale? 


# Create renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.ResetCamera()

# Enable user interaction
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# Add spheres to the renderer
debt_actor = create_sphere(0.5, [1.0, 0.0, 0.0], [-2.0, 0.0, 0.0])  # Debt sphere
revenue_actor = create_sphere(0.5, [0.0, 1.0, 0.0], [0.0, 0.0, 0.0])  # Revenue sphere
expenses_actor = create_sphere(0.5, [0.0, 0.0, 1.0], [2.0, 0.0, 0.0])  # Expenses sphere
net_income_actor = create_sphere(0.5, [1.0, 1.0, 0.0], [4.0, 0.0, 0.0])  # Net Income sphere

renderer.AddActor(debt_actor)
renderer.AddActor(revenue_actor)
renderer.AddActor(expenses_actor)
renderer.AddActor(net_income_actor)

# Enable user interaction
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.Initialize()

style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

render_window.Render()

# Animation parameters
animation_duration = 60  # Duration in seconds
animation_steps = 5  # Number of steps for the animation


loop_count = 10  # Number of times to loop the animation

loop_iteration = 0

# Initialize variables for GIF creation
image_list = []

# Update function
def update():
    global debt, revenue, expenses, net_income, loop_iteration, start_time

    # Update the values
    debt, revenue, expenses, net_income = update_revenue_and_expenses(debt, revenue, expenses, loop_iteration, time_scale)

    scale_factor = 0.00002  # Experiment with different values to ensure sphere visibility

    debt_actor.SetScale(debt * scale_factor, debt * scale_factor, debt * scale_factor)

    revenue_actor.SetScale(revenue * scale_factor, revenue * scale_factor, revenue * scale_factor)
    expenses_actor.SetScale(expenses * scale_factor, expenses * scale_factor, expenses * scale_factor)
    net_income_actor.SetScale(net_income * scale_factor, net_income * scale_factor, net_income * scale_factor)
    print(f"Period: {loop_iteration}, Debt: {debt:.2f}, Net Income: {net_income:.2f}")

    render_window.Render()

    loop_iteration += 1
    
    #if loop_iteration >= animation_steps:
        #loop_iteration = 0

    if debt <= 0:
        interactor.DestroyTimer(timer_id)  # Stop the timer when debt is zero or less
        print("Debt reached zero or below. Stopping the animation.")
        imageio.mimsave("F:\valuation_models\output\animation.gif", image_list)
        
    else:
        # Capture the current frame and append it to the list
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(render_window)
        w2if.Update()
        writer = vtk.vtkPNGWriter()
        writer.SetInputConnection(w2if.GetOutputPort())
        filename = f"F:\valuation_models\output\frame_{loop_iteration}.png"
        writer.SetFileName(filename)
        writer.Write()

        # Append the filename to the list
        image_list.append(filename)    

    render_window.Render()
    
    # Check if 30 seconds have passed
    #current_time = time.time()
    #if current_time - start_time >= 30:
        #interactor.DestroyTimer(timer_id)  # Stop the timer

# Create a timer to control the animation for 30 seconds
start_time = time.time()  # Start time of the animation

# Call the update function at regular intervals
timer_id = interactor.CreateRepeatingTimer(int(1000 / animation_steps))
interactor.AddObserver('TimerEvent', lambda caller, event: update())

# Start the interactor
interactor.Start()

#Save GIF
# Set up the animation scene writer to save the animation as a GIF
writer = vtk.vtkAnimationSceneImageWriter()
writer.SetFileName("F:\valuation_models\output\animation.gif")
writer.SetFrameRate(30)  # Set the frame rate for the GIF

# Start the render and the writer
writer.SetInput(render_window)
writer.Write()

