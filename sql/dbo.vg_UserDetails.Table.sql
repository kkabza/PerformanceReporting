USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_UserDetails]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_UserDetails](
	[UserId] [uniqueidentifier] NOT NULL,
	[FirstName] [varchar](30) NOT NULL,
	[LastName] [varchar](30) NOT NULL,
	[Title] [varchar](30) NOT NULL,
	[Company] [varchar](50) NOT NULL,
	[Address] [varchar](50) NOT NULL,
	[City] [varchar](40) NOT NULL,
	[State] [char](2) NOT NULL,
	[ZipCode] [varchar](15) NOT NULL,
	[Telephone] [varchar](15) NOT NULL,
	[AccountBalance] [money] NOT NULL,
	[UserIP] [varchar](20) NULL,
 CONSTRAINT [PK_vg_UserDetails] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_UserDetails] ADD  CONSTRAINT [DF_vg_UserDetails_AccountBalance]  DEFAULT ((0.00)) FOR [AccountBalance]
GO
ALTER TABLE [dbo].[vg_UserDetails]  WITH CHECK ADD  CONSTRAINT [FK_vg_UserDetails_aspnet_Users] FOREIGN KEY([UserId])
REFERENCES [dbo].[aspnet_Users] ([UserId])
GO
ALTER TABLE [dbo].[vg_UserDetails] CHECK CONSTRAINT [FK_vg_UserDetails_aspnet_Users]
GO
