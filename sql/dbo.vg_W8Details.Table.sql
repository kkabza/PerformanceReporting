USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_W8Details]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_W8Details](
	[UserId] [uniqueidentifier] NOT NULL,
	[W8Id] [int] IDENTITY(1,1) NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[DateCreated] [datetime] NOT NULL,
	[Active] [bit] NOT NULL,
	[VGProductID] [int] NOT NULL,
	[DateModified] [datetime] NULL,
 CONSTRAINT [PK_vg_W8Details] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC,
	[VGProductID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
