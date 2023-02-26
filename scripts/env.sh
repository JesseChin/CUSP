ip=$(
    ifconfig eth0 | awk '/inet /{print $2}' | cut -f2 -d':'
)
