print(new_X_Y)
X=[i[0] for i in new_X_Y]
Y=[i[1] for i in new_X_Y]
plt.plot(X,Y)
plt.xlabel('Velocity')
plt.ylabel('Flow')
plt.title('Velocity vs Flow')
plt.show()